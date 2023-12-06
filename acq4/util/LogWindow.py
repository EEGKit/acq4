import json
import os
import re
import subprocess
import sys
import traceback
import weakref
from datetime import datetime
from threading import RLock
from typing import Union, Optional

import numpy as np
import six
from six.moves import map
from six.moves import range

if __name__ == "__main__":
    libdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path = [os.path.join(libdir, "lib", "util")] + sys.path + [libdir]

import pyqtgraph.configfile as configfile
from acq4.util import Qt
from acq4.util.DataManager import DirHandle
from acq4.util.HelpfulException import HelpfulException
from acq4.util.debug import printExc
from acq4.util.codeEditor import invokeCodeEditor
from pyqtgraph import FeedbackButton
from pyqtgraph import FileDialog

LogWidgetTemplate = Qt.loadUiType(os.path.join(os.path.dirname(__file__), "LogWidgetTemplate.ui"))[0]


Stylesheet = """
    body {color: #000; font-family: sans;}
    .entry {}
    .error .message {color: #900}
    .warning .message {color: #740}
    .user .message {color: #009}
    .status .message {color: #090}
    .logExtra {margin-left: 40px;}
    .traceback {color: #555; height: 0px;}
    .timestamp {color: #000;}
"""

pageTemplate = f"""
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style type="text/css">
{Stylesheet}    </style>
    
    <script type="text/javascript">
        function showDiv(id) {{
            div = document.getElementById(id);
            div.style.visibility = "visible";
            div.style.height = "auto";
        }}
    </script>
</head>
<body>
</body>
</html>
"""


WIN: Optional["LogWindow"] = None


class LogButton(FeedbackButton):
    def __init__(self, *args):
        FeedbackButton.__init__(self, *args)

        global WIN
        self.clicked.connect(WIN.show)
        WIN.buttons.append(weakref.ref(self))


class LogWindow(Qt.QMainWindow):
    """LogWindow contains a LogWidget inside a window. LogWindow is responsible for collecting messages generated by
    the program/user, formatting them into a nested dictionary, and saving them in a log.txt file. The LogWidget
    takes care of displaying messages.
    
    Messages can be logged by calling logMsg or logExc functions from acq4.Manager. These functions call the
    LogWindow.logMsg and LogWindow.logExc functions, but other classes should not call the LogWindow functions
    directly.
    
    """

    sigLogMessage = Qt.Signal(object)

    def __init__(self, manager):
        global WIN
        Qt.QMainWindow.__init__(self)
        WIN = self
        self.setWindowTitle("Log")
        path = os.path.dirname(__file__)
        self.setWindowIcon(Qt.QIcon(os.path.join(path, "logIcon.png")))
        self.wid = LogWidget(self, manager)
        self.wid.ui.input = Qt.QLineEdit()
        self.wid.ui.gridLayout.addWidget(self.wid.ui.input, 2, 0, 1, 3)
        self.wid.ui.dirLabel.setText("Current Storage Directory: None")
        self.setCentralWidget(self.wid)
        self.resize(1000, 500)
        self.manager = manager
        self.entriesSaved = 0
        self.entriesVisible = 0
        self.logFile = None
        # start a new temp log file, destroying anything left over from the last session.
        configfile.writeConfigFile("", self.fileName())
        # weak references to all Log Buttons get added to this list, so it's easy to make them all do things, like flash red.
        self.buttons = []
        self.lock = RLock()
        self.errorDialog = ErrorDialog()

        self.wid.ui.input.returnPressed.connect(self.textEntered)
        self.sigLogMessage.connect(self.queuedLogMsg, Qt.Qt.QueuedConnection)

    def queuedLogMsg(self, args):  # called indirectly when logMsg is called from a non-gui thread
        self.logMsg(*args[0], **args[1])

    def logMsg(self, msg, importance=5, msgType="status", **kwargs):
        """
        msg: the text of the log message
        msgTypes: user, status, error, warning (status is default)
        importance: 0-9 (0 is low importance, 9 is high, 5 is default)
        other keywords:
          exception: a tuple (type, exception, traceback) as returned by sys.exc_info()
          excInfo: an object with attributes exc_type, exc_value, exc_traceback, and thread
          docs: a list of strings where documentation related to the message can be found
          reasons: a list of reasons (as strings) for the message
          traceback: a list of formatted callstack/trackback objects (formatting a traceback/callstack returns a
              list of strings), usually looks like [['line 1', 'line 2', 'line3'], ['line1', 'line2']]
           Feel free to add your own keyword arguments. These will be saved in the log.txt file, but will not affect the
           content or way that messages are displayed.
        """

        # for thread-safetyness:
        isGuiThread = Qt.QThread.currentThread() == Qt.QCoreApplication.instance().thread()
        if not isGuiThread:
            self.sigLogMessage.emit(((msg, importance, msgType), kwargs))
            return

        try:
            currentDir = self.manager.getCurrentDir()
        except:
            currentDir = None
        if isinstance(currentDir, DirHandle):
            kwargs["currentDir"] = currentDir.name()
        else:
            kwargs["currentDir"] = None

        now = datetime.now().astimezone().isoformat()
        saveName = f"LogEntry_{self.entriesSaved}"
        with self.lock:
            self.entriesSaved += 1
            self.entriesVisible += 1
            savedId = self.entriesSaved
            entry = {
                "message": msg,
                "timestamp": now,
                "importance": importance,
                "msgType": msgType,
                "id": self.entriesVisible,
            }
        for k in kwargs:
            entry[k] = kwargs[k]

        self.processEntry(entry)

        # Allow exception to override values in the entry
        if entry.get("exception", None) is not None and "msgType" in entry["exception"]:
            entry["msgType"] = entry["exception"]["msgType"]

        self.saveEntries({saveName: {**entry, "id": savedId}})
        self.wid.addEntry(entry)  # takes care of displaying the entry if it passes the current filters on the logWidget

        if entry["msgType"] == "error" and self.errorDialog.show(entry) is False:
            self.flashButtons()

    def logExc(self, *args, **kwargs):
        """Calls logMsg, but adds in the current exception and callstack. Must be called within an except block,
        and should only be called if the exception is not re-raised. Unhandled exceptions, or exceptions that reach
        the top of the callstack are automatically logged, so logging an exception that will be re-raised can cause
        the exception to be logged twice. Takes the same arguments as logMsg. """
        kwargs["exception"] = sys.exc_info()
        kwargs["traceback"] = traceback.format_stack()[:-2] + ["------- exception caught ---------->\n"]
        self.logMsg(*args, **kwargs)

    def processEntry(self, entry):
        # pre-processing common to saveEntry and displayEntry

        # convert exc_info to serializable dictionary
        if entry.get("exception", None) is not None:
            excInfo = entry.pop("exception")
            entry["exception"] = self.exceptionToDict(*excInfo, thread=None, topTraceback=entry.get("traceback", []))
        elif entry.get("excInfo", None) is not None:
            excInfo = entry.pop("excInfo")
            entry["exception"] = self.exceptionToDict(
                excInfo.exc_type,
                excInfo.exc_value,
                excInfo.exc_traceback,
                excInfo.thread,
                topTraceback=entry.get("traceback", [])
            )
        else:
            entry["exception"] = None

    def textEntered(self):
        msg = six.text_type(self.wid.ui.input.text())
        if msg == "!!":
            self.makeError1()
        elif msg == "##":
            self.makeErrorLogExc()
        try:
            currentDir = self.manager.getCurrentDir()
        except:
            currentDir = None
        self.logMsg(msg, importance=8, msgType="user", currentDir=currentDir)
        self.wid.ui.input.clear()

    def exceptionToDict(self, exType, exc, tb, thread, topTraceback):
        excDict = {
            "message": traceback.format_exception(exType, exc, tb)[-1][:-1],
            "traceback": topTraceback + traceback.format_exception(exType, exc, tb)[:-1],
            # "thread": thread,
        }
        if hasattr(exc, "docs") and len(exc.docs) > 0:
            excDict["docs"] = exc.docs
        if hasattr(exc, "reasons") and len(exc.reasons) > 0:
            excDict["reasons"] = exc.reasons
        if hasattr(exc, "kwargs"):
            for k in exc.kwargs:
                excDict[k] = exc.kwargs[k]
        if hasattr(exc, "oldExc"):
            excDict["oldExc"] = self.exceptionToDict(*exc.oldExc, thread=None, topTraceback=[])
        return excDict

    def flashButtons(self):
        for b in self.buttons:
            if b() is not None:
                b().failure(tip="An error occurred. Please see the log.", limitedTime=False)

    def resetButtons(self):
        for b in self.buttons:
            if b() is not None:
                b().reset()

    def makeError1(self):
        try:
            self.makeError2()
            # print x
        except:
            t, exc, tb = sys.exc_info()
            raise HelpfulException(
                message="This button does not work.",
                exc=(t, exc, tb),
                reasons=["It's supposed to raise an error for testing purposes", "You're doing it wrong."],
            )

    def makeErrorLogExc(self):
        try:
            raise NameError("name 'y' is not defined")
        except:
            self.logExc("This is the message sent to logExc", msgType="error")

    def makeError2(self):
        try:
            raise NameError("name 'y' is not defined")
        except:
            t, exc, tb = sys.exc_info()
            raise HelpfulException(
                message="msg from makeError",
                exc=(t, exc, tb),
                reasons=["reason one", "reason 2"],
                docs=["what, you expect documentation?"],
            )

    def show(self):
        Qt.QMainWindow.show(self)
        self.activateWindow()
        self.raise_()
        self.resetButtons()

    def fileName(self):
        # return the log file currently used
        if self.logFile is None:
            return "tempLog.txt"
        else:
            return self.logFile.name()

    def setLogDir(self, dh: DirHandle):
        """
        Move ongoing log operations to a different directory. Creates the log.txt file if needed. Temporary log entries
        (from before a log dir was set) will be appended to log.txt. Display in the log window will remain unchanged.
        Thereafter, new log entries will be appended to the new log file.
        """
        if self.fileName() == dh.name():
            return

        # make these notes before we change the log file, so when a log ends, you know where it went after.
        self.logMsg(f"Moving log storage to {dh.name(relativeTo=self.manager.baseDir)}.")
        if self.logFile is not None:
            self.logMsg(f"Previous log storage was {self.logFile.name(relativeTo=self.manager.baseDir)}.")

        oldfName = self.fileName()
        if oldfName == "tempLog.txt":
            with self.lock:
                temp = configfile.readConfigFile(oldfName)
        else:  # already saved log messages needn't be copied into the new file
            temp = {}

        with self.lock:
            if dh.exists("log.txt"):
                self.logFile = dh["log.txt"]
                try:
                    tempCount = max(e["id"] for e in configfile.readConfigFile(self.logFile.name()).values())
                except IndexError:
                    tempCount = 0
                newTemp = {}
                for v in temp.values():
                    # renumber the entries to be relative to the existing file
                    tempCount += 1
                    v["id"] = tempCount
                    newTemp[f"LogEntry_{tempCount}"] = v
                self.saveEntries(newTemp)
                self.entriesSaved = tempCount
            else:
                self.logFile = dh.createFile("log.txt")
                self.saveEntries(temp)

        self.logMsg(f"Moved log storage from {oldfName} to {self.fileName()}.")
        self.logMsg(f"Current configuration: {json.dumps(self.manager.config)}")
        self.wid.ui.dirLabel.setText("Current Storage Directory: " + self.fileName())
        self.manager.sigLogDirChanged.emit(dh)

    def getLogDir(self):
        if self.logFile is None:
            return None
        else:
            return self.logFile.parent()

    def saveEntries(self, entry):
        with self.lock:
            configfile.appendConfigFile(entry, self.fileName())

    def disablePopups(self, disable):
        self.errorDialog.disable(disable)


class LogWidget(Qt.QWidget):
    dirFilter: Union[str, bool]
    sigDisplayEntry = Qt.Signal(object)  # for thread-safetyness
    sigAddEntry = Qt.Signal(object)  # for thread-safetyness
    sigScrollToAnchor = Qt.Signal(object)  # for internal use.

    def __init__(self, parent, manager):
        Qt.QWidget.__init__(self, parent)
        self.ui = LogWidgetTemplate()
        self.manager = manager
        self.ui.setupUi(self)
        self.ui.filterTree.topLevelItem(1).setExpanded(True)

        self.entries = []  # stores all log entries in memory
        self.cache = {}  # for storing html strings of entries that have already been processed
        self.displayedEntries = []
        self.typeFilters = []
        self.importanceFilter = 0
        self.dirFilter = False
        self.entryArrayBuffer = np.zeros(
            1000,
            dtype=[  # a record array for quick filtering of entries
                ("index", "int32"),
                ("importance", "int32"),
                ("msgType", "|S10"),
                ("directory", "|S100"),
                ("entryId", "int32"),
            ],
        )
        self.entryArray = self.entryArrayBuffer[:0]

        self.filtersChanged()

        self.sigDisplayEntry.connect(self.displayEntry, Qt.Qt.QueuedConnection)
        self.sigAddEntry.connect(self.addEntry, Qt.Qt.QueuedConnection)
        self.ui.exportHtmlBtn.clicked.connect(self.exportHtml)
        self.ui.filterTree.itemChanged.connect(self.setCheckStates)
        self.ui.importanceSlider.valueChanged.connect(self.filtersChanged)
        self.ui.output.anchorClicked.connect(self.linkClicked)
        self.sigScrollToAnchor.connect(self.scrollToAnchor, Qt.Qt.QueuedConnection)

    def loadFile(self, f):
        """Load the file, f. f must be able to be read by configfile.py"""
        logConf = configfile.readConfigFile(f)
        self.entries = []
        self.entryArrayBuffer = np.zeros(
            len(logConf),
            dtype=[
                ("index", "int32"),
                ("importance", "int32"),
                ("msgType", "|S10"),
                ("directory", "|S100"),
                ("entryId", "int32"),
            ],
        )
        self.entryArray = self.entryArrayBuffer[:]

        for i, (k, v) in enumerate(logConf.items()):
            v["id"] = k[9:]  # record unique ID to facilitate HTML generation (javascript needs this ID)
            self.entries.append(v)
            self.entryArray[i] = np.array(
                [
                    (
                        i,
                        v.get("importance", 5),
                        v.get("msgType", "status"),
                        v.get("currentDir", ""),
                        v.get("entryId", v["id"]),
                    )
                ],
                dtype=[
                    ("index", "int32"),
                    ("importance", "int32"),
                    ("msgType", "|S10"),
                    ("directory", "|S100"),
                    ("entryId", "int32"),
                ],
            )
        self.filterEntries()  # puts all entries through current filters and displays the ones that pass

    def addEntry(self, entry):
        # All incoming messages begin here

        # for thread-safetyness:
        isGuiThread = Qt.QThread.currentThread() == Qt.QCoreApplication.instance().thread()
        if not isGuiThread:
            self.sigAddEntry.emit(entry)
            return

        self.entries.append(entry)
        i = len(self.entryArray)

        entryDir = entry.get("currentDir", None)
        if entryDir is None:
            entryDir = ""

        arr = np.array(
            [(i, entry["importance"], entry["msgType"], entryDir, entry["id"])],
            dtype=[
                ("index", "int32"),
                ("importance", "int32"),
                ("msgType", "|S10"),
                ("directory", "|S100"),
                ("entryId", "int32"),
            ],
        )

        # make more room if needed
        if len(self.entryArrayBuffer) == len(self.entryArray):
            newArray = np.empty(len(self.entryArrayBuffer) + 1000, self.entryArrayBuffer.dtype)
            newArray[: len(self.entryArray)] = self.entryArray
            self.entryArrayBuffer = newArray
        self.entryArray = self.entryArrayBuffer[: len(self.entryArray) + 1]
        self.entryArray[i] = arr
        self.checkDisplay(entry)  # displays the entry if it passes the current filters

    def setCheckStates(self, item, column):
        if item == self.ui.filterTree.topLevelItem(1):
            if item.checkState(0):
                for i in range(item.childCount()):
                    item.child(i).setCheckState(0, Qt.Qt.Checked)
        elif item.parent() == self.ui.filterTree.topLevelItem(1):
            if not item.checkState(0):
                self.ui.filterTree.topLevelItem(1).setCheckState(0, Qt.Qt.Unchecked)
        self.filtersChanged()

    def filtersChanged(self):
        # Update self.typeFilters, self.importanceFilter, and self.dirFilter to reflect changes.
        tree = self.ui.filterTree

        self.typeFilters = []
        for i in range(tree.topLevelItem(1).childCount()):
            child = tree.topLevelItem(1).child(i)
            if tree.topLevelItem(1).checkState(0) or child.checkState(0):
                text = child.text(0)
                self.typeFilters.append(six.text_type(text))

        self.importanceFilter = self.ui.importanceSlider.value()

        self.updateDirFilter()

        self.filterEntries()

    def updateDirFilter(self, dh=None):
        if self.ui.filterTree.topLevelItem(0).checkState(0):
            if dh is None:
                self.dirFilter = self.manager.getDirOfSelectedFile().name()
            else:
                self.dirFilter = dh.name()
        else:
            self.dirFilter = False

    def filterEntries(self):
        """Runs each entry in self.entries through the filters and displays if it makes it through."""
        # make self.entries a record array, then filtering will be much faster (to OR true/false arrays, + them)
        # TODO FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
        typeMask = self.entryArray["msgType"] == ""
        for t in self.typeFilters:
            typeMask += self.entryArray["msgType"] == t
        mask = (self.entryArray["importance"] > self.importanceFilter) * typeMask
        if self.dirFilter is not False:
            _d = np.ascontiguousarray(self.entryArray["directory"])
            j = len(self.dirFilter)
            i = len(_d)
            _d = _d.view(np.byte).reshape(i, 100)[:, :j]
            _d = _d.reshape(i * j).view("|S%d" % j)
            mask *= _d == self.dirFilter

        self.ui.output.clear()
        global Stylesheet
        self.ui.output.document().setDefaultStyleSheet(Stylesheet)
        indices = list(self.entryArray[mask]["index"])
        self.displayEntry([self.entries[i] for i in indices])

    def checkDisplay(self, entry):
        # checks whether entry passes the current filters and displays it if it does.
        if entry["msgType"] not in self.typeFilters:
            return
        elif entry["importance"] < self.importanceFilter:
            return
        elif self.dirFilter is not False:
            if entry["currentDir"][: len(self.dirFilter)] != self.dirFilter:
                return
        else:
            self.displayEntry([entry])

    def displayEntry(self, entries):
        # entries should be a list of log entries

        # for thread-safetyness:
        isGuiThread = Qt.QThread.currentThread() == Qt.QCoreApplication.instance().thread()
        if not isGuiThread:
            self.sigDisplayEntry.emit(entries)
            return

        for entry in entries:
            if id(entry) not in self.cache:
                self.cache[id(entry)] = self.generateEntryHtml(entry)

            html = self.cache[id(entry)]
            sb = self.ui.output.verticalScrollBar()
            isMax = sb.value() == sb.maximum()

            self.ui.output.append(html)
            self.displayedEntries.append(entry)

            if isMax:
                # can't scroll to end until the web frame has processed the html change
                # frame.setScrollBarValue(Qt.Qt.Vertical, frame.scrollBarMaximum(Qt.Qt.Vertical))

                # Calling processEvents anywhere inside an error handler is forbidden
                # because this can lead to Qt complaining about paint() recursion.
                # Qt.QApplication.processEvents()
                # self.ui.output.scrollToAnchor(str(entry['id']))

                self.sigScrollToAnchor.emit(str(entry["id"]))  # queued connection
            # self.ui.logView.update()

    def scrollToAnchor(self, anchor):
        self.ui.output.scrollToAnchor(anchor)

    def generateEntryHtml(self, entry):
        msg = self.cleanText(entry["message"])

        reasons = ""
        docs = ""
        exc = ""
        if "reasons" in entry:
            reasons = self.formatReasonStrForHTML(entry["reasons"])
        if "docs" in entry:
            docs = self.formatDocsStrForHTML(entry["docs"])
        if entry.get("exception", None) is not None:
            exc = self.formatExceptionForHTML(entry, entryId=entry["id"])

        extra = reasons + docs + exc
        if extra != "":
            # extra = "<div class='logExtra'>" + extra + "</div>"
            extra = "<table class='logExtra'><tr><td>" + extra + "</td></tr></table>"

        return """
        <a name="%s"/><table class='entry'><tr><td>
            <table class='%s'><tr><td>
                <span class='timestamp'>%s</span>
                <span class='message'>%s</span>
                %s
            </td></tr></table>
        </td></tr></table>
        """ % (
            str(entry["id"]),
            entry["msgType"],
            entry["timestamp"],
            msg,
            extra,
        )

    @staticmethod
    def cleanText(text):
        text = re.sub(r"&", "&amp;", text)
        text = re.sub(r">", "&gt;", text)
        text = re.sub(r"<", "&lt;", text)
        text = re.sub(r"\n", "<br/>\n", text)

        # replace indenting spaces with &nbsp
        lines = text.split('\n')
        indents = ['&nbsp;' * (len(line) - len(line.lstrip())) for line in lines]
        lines = [indent + line.lstrip() for indent, line in zip(indents, lines)]
        text = ''.join(lines)

        return text

    def formatExceptionForHTML(self, entry, exception=None, count=1, entryId=None):
        # Here, exception is a dict that holds the message, reasons, docs, traceback and oldExceptions (which are
        # also dicts, with the same entries). The count and tracebacks keywords are for calling recursively.
        if exception is None:
            exception = entry["exception"]

        text = self.cleanText(exception["message"])
        text = re.sub(r"^HelpfulException: ", "", text)
        messages = [text]

        if "reasons" in exception:
            reasons = self.formatReasonsStrForHTML(exception["reasons"])
            text += reasons
        if "docs" in exception:
            docs = self.formatDocsStrForHTML(exception["docs"])
            text += docs

        stackText = [self.formatTracebackForHTML(exception["traceback"])]
        text = [text]

        if "oldExc" in exception:
            exc, tb, msgs = self.formatExceptionForHTML(entry, exception["oldExc"], count=count + 1)
            text.extend(exc)
            messages.extend(msgs)
            stackText.extend(tb)

        if count != 1:
            return text, stackText, messages
        exc = '<div class="exception"><ol>' + "\n".join(["<li>%s</li>" % ex for ex in text]) + "</ol></div>"
        tbStr = "\n".join(
            [
                "<li><b>%s</b><br/><span class='traceback'>%s</span></li>" % (messages[i], tb)
                for i, tb in enumerate(stackText)
            ]
        )
        entry["tracebackHtml"] = tbStr

        return f'{exc}<a href="exc:{entryId}">Show traceback {entryId}</a>'

    def formatTracebackForHTML(self, tb):
        try:
            tb = [line for line in tb if not line.startswith("Traceback (most recent call last)")]
        except Exception:
            print("\n" + str(tb) + "\n")
            raise

        cleanLines = []
        for i, line in enumerate(tb):
            line = self.cleanText(line)
            m = re.match(r"(.*)File \"(.*)\", line (\d+)", line)
            if m is not None:
                # insert hyperlink for opening file in editor
                indent, codeFile, lineNum = m.groups()
                extra = line[m.end():]
                line = f'{indent}File <a href="code:{lineNum}:{codeFile}">{codeFile}</a>, line {lineNum}{extra}'
            cleanLines.append(line)
        return ''.join(cleanLines)

    def formatReasonsStrForHTML(self, reasons):
        # indent = 6
        reasonStr = "<table class='reasons'><tr><td>Possible reasons include:\n<ul>\n"
        for r in reasons:
            r = self.cleanText(r)
            reasonStr += f"<li>{r}" + "</li>\n"
        reasonStr += "</ul></td></tr></table>\n"
        return reasonStr

    def formatDocsStrForHTML(self, docs):
        # indent = 6
        docStr = "<div class='docRefs'>Relevant documentation:\n<ul>\n"
        for _d in docs:
            _d = self.cleanText(_d)
            docStr += '<li><a href="doc:%s">%s</a></li>\n' % (_d, _d)
        docStr += "</ul></div>\n"
        return docStr

    def exportHtml(self, fileName=False):
        if fileName is False:
            self.fileDialog = FileDialog(self, "Save HTML as...", self.manager.getCurrentDir().name())
            self.fileDialog.setAcceptMode(Qt.QFileDialog.AcceptSave)
            self.fileDialog.show()
            self.fileDialog.fileSelected.connect(self.exportHtml)
            return
        if fileName[-5:] != ".html":
            fileName += ".html"

        global pageTemplate
        doc = pageTemplate
        for e in self.displayedEntries:
            doc += self.cache[id(e)]
        for e in self.displayedEntries:
            if "tracebackHtml" in e:
                doc = re.sub(
                    f'<a href="exc:{e["id"]}">(<[^>]+>)*Show traceback {e["id"]}(<[^>]+>)*</a>',
                    e["tracebackHtml"],
                    doc,
                )

        with open(fileName, "wb") as f:
            f.write(doc.encode("utf-8"))

    def makeError1(self):
        # just for testing error logging
        try:
            self.makeError2()
        except:
            printExc("This is the message sent to printExc.")

    def makeError2(self):
        # just for testing error logging
        try:
            raise NameError("name 'y' is not defined")
        except:
            t, exc, tb = sys.exc_info()
            raise HelpfulException(
                message="msg from makeError",
                exc=(t, exc, tb),
                reasons=["reason one", "reason 2"],
                docs=["what, you expect documentation?"],
            )

    def linkClicked(self, url):
        action = url.scheme()
        target = url.path()
        if action == "doc":
            self.manager.showDocumentation(target)
        elif action == "exc":
            cursor = self.ui.output.document().find(f"Show traceback {target}")
            try:
                tb = self.entries[int(target) - 1]["tracebackHtml"]
            except IndexError:
                try:
                    matchingEntry = self.entryArray[(self.entryArray["entryId"] == (int(target)))]
                    tb = self.entries[int(matchingEntry["index"])]["tracebackHtml"]
                except IndexError:
                    print("requested index %d, but only %d entries exist." % (int(target) - 1, len(self.entries)))
                    raise
            cursor.insertHtml(tb)
        elif action == 'code':
            lineNum, _, codeFile = target.partition(':')
            invokeCodeEditor(fileName=codeFile, lineNum=lineNum)


    def clear(self):
        self.ui.output.clear()
        self.displayedEntries = []


class ErrorDialog(Qt.QDialog):
    def __init__(self):
        Qt.QDialog.__init__(self)
        self.setWindowFlags(Qt.Qt.Window)
        self.setWindowTitle("ACQ4 Error")
        self.layout = Qt.QVBoxLayout()
        self.layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(self.layout)
        self.messages = []

        self.msgLabel = Qt.QLabel()
        self.msgLabel.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        self.layout.addWidget(self.msgLabel)
        self.msgLabel.setMaximumWidth(800)
        self.msgLabel.setMinimumWidth(500)
        self.msgLabel.setWordWrap(True)
        self.layout.addStretch()
        self.disableCheck = Qt.QCheckBox("Disable error message popups")
        self.layout.addWidget(self.disableCheck)

        self.btnLayout = Qt.QHBoxLayout()
        self.btnLayout.addStretch()
        self.okBtn = Qt.QPushButton("OK")
        self.btnLayout.addWidget(self.okBtn)
        self.nextBtn = Qt.QPushButton("Show next error")
        self.btnLayout.addWidget(self.nextBtn)
        self.nextBtn.hide()
        self.logBtn = Qt.QPushButton("Show Log...")
        self.btnLayout.addWidget(self.logBtn)
        self.btnLayoutWidget = Qt.QWidget()
        self.layout.addWidget(self.btnLayoutWidget)
        self.btnLayoutWidget.setLayout(self.btnLayout)
        self.btnLayout.addStretch()

        self.okBtn.clicked.connect(self.okClicked)
        self.nextBtn.clicked.connect(self.nextMessage)
        self.logBtn.clicked.connect(self.logClicked)

    def show(self, entry):
        # rules are:
        #   - Try to show friendly error messages
        #   - If there are any helpfulExceptions, ONLY show those
        #     otherwise, show everything
        self.lastEntry = entry

        msgLines = []
        if entry["message"] is not None:
            msgLines.append(entry["message"])

        # extract list of exceptions
        key = "exception"
        exc = entry
        while key in exc:
            exc = exc[key]

            if exc is None:
                break

            # ignore this error if it was generated on the command line.
            tb = exc.get("traceback", ["", ""])
            if len(tb) > 1 and 'File "<stdin>"' in tb[1]:
                return False

            key = "oldExc"
            if exc["message"].startswith("HelpfulException"):
                msgLines.append("<b>" + self.cleanText(re.sub(r"^HelpfulException: ", "", exc["message"])) + "</b>")
            elif exc["message"] == "None":
                continue
            else:
                msgLines.append(self.cleanText(exc["message"]))

        msg = "<br>".join(msgLines)

        if self.disableCheck.isChecked():
            return False
        if self.isVisible():
            self.messages.append(msg)
            self.nextBtn.show()
            self.nextBtn.setEnabled(True)
            self.nextBtn.setText("Show next error (%d more)" % len(self.messages))
        else:
            w = Qt.QApplication.activeWindow()
            self.nextBtn.hide()
            self.msgLabel.setText(msg)
            self.open()
            if w is not None:
                cp = w.geometry().center()
                self.setGeometry(int(cp.x() - self.width() / 2.0), int(cp.y() - self.height() / 2.0), self.width(), self.height())
        self.raise_()

    @staticmethod
    def cleanText(text):
        text = re.sub(r"&", "&amp;", text)
        text = re.sub(r">", "&gt;", text)
        text = re.sub(r"<", "&lt;", text)
        text = re.sub(r"\n", "<br/>\n", text)
        return text

    def closeEvent(self, ev):
        Qt.QDialog.closeEvent(self, ev)
        self.messages = []

    def okClicked(self):
        self.accept()
        self.messages = []

    def logClicked(self):
        global WIN
        self.accept()
        WIN.show()
        self.messages = []

    def nextMessage(self):
        self.msgLabel.setText(self.messages.pop(0))
        self.nextBtn.setText("Show next error (%d more)" % len(self.messages))
        if len(self.messages) == 0:
            self.nextBtn.setEnabled(False)

    def disable(self, disable):
        self.disableCheck.setChecked(disable)


if __name__ == "__main__":
    app = Qt.QApplication([])
    log = LogWindow(None)
    log.show()
    original_excepthook = sys.excepthook

    def excepthook(*args):
        global original_excepthook
        log.displayException(*args)
        original_excepthook(*args)
        sys.last_traceback = None  # the important bit

    sys.excepthook = excepthook

    app.exec_()
