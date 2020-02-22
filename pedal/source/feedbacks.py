from pedal.core.commands import feedback
from pedal.core.feedback import AtomicFeedbackFunction
from pedal.core.report import MAIN_REPORT
from pedal.utilities.exceptions import ExpandedTraceback
from pedal.source.constants import TOOL_NAME


@AtomicFeedbackFunction(title="No Source Code",
                        text_template="Source code file is blank.".format,
                        justification="After stripping the code, there were no characters.")
def blank_source(group=None, report=MAIN_REPORT):
    return feedback(blank_source.__name__, category=feedback.CATEGORIES.SYNTAX, tool=TOOL_NAME,
                    title=blank_source.title, version=blank_source.version,
                    group=group, message=blank_source.text_template(), report=report)


@AtomicFeedbackFunction(title="Not Enough Sections",
                        text_template=("Tried to advance to next section but the "
                                       "section was not found. Tried to load section "
                                       "{count}, but there were only {found} sections.").format,
                        justification="Section index exceeded the length of the separated sections list.")
def not_enough_sections(section_number, found, report=MAIN_REPORT):
    fields = {'count': section_number, 'found': found}
    return feedback(not_enough_sections.__name__, category=feedback.CATEGORIES.SYNTAX, tool=TOOL_NAME,
                    title=not_enough_sections.title, version=not_enough_sections.version,
                    fields=fields,
                    message=not_enough_sections.text_template(**fields), report=report)


@AtomicFeedbackFunction(title='Source File Not Found',
                        text_template=("The given filename ('{filename}') was either not found"
                                       " or could not be opened. Please make sure the file is"
                                       " available.").format,
                        version='0.0.1',
                        justification="IOError while opening file to set_source")
def source_file_not_found(filename, sections, report=MAIN_REPORT):
    fields = {'filename': filename, 'sections': sections}
    return feedback(source_file_not_found.__name__, category=feedback.CATEGORIES.SYNTAX, tool=TOOL_NAME,
                    title=source_file_not_found.TITLE, version=source_file_not_found.VERSION,
                    fields=fields,
                    text=source_file_not_found.TEXT_TEMPLATE(**fields),
                    group=0 if sections else None,
                    report=report)


@AtomicFeedbackFunction(title="Syntax Error",
                        message_template="```\n{context}\n```\nBad syntax on line {lineno}".format,
                        text_template="{context}\nBad syntax on line {lineno}".format,
                        version='0.0.1',
                        justification="Syntax error was triggered while calling ast.parse")
def syntax_error(line, filename, code, offset, text, traceback, exception, exc_info, report=MAIN_REPORT, muted=False):
    traceback = ExpandedTraceback(exception, exc_info, traceback, report.submission.instructor_file,
                                  line, filename, code)
    context = traceback.format_exception()
    fields = {'lineno': line, 'filename': filename, 'offset': offset, 'text': text,
              'traceback': traceback, 'exception': exception, 'context': context}
    return feedback(syntax_error.__name__, category=feedback.CATEGORIES.SYNTAX, tool=TOOL_NAME,
                    title=syntax_error.title, version=syntax_error.version,
                    fields=fields,
                    message=syntax_error.message_template(**fields),
                    text=syntax_error.text_template(**fields), muted=muted,
                    locations=line,
                    report=report)


@AtomicFeedbackFunction(title="Incorrect Number of Sections",
                        text_template=("Incorrect number of sections in your file. "
                                       "Expected {count}, but only found {found}").format,
                        justification="")
def incorrect_number_of_sections(count, found, group, report=MAIN_REPORT):
    fields = {'count': count, 'found': found}
    return feedback(incorrect_number_of_sections.__name__, category=feedback.CATEGORIES.SYNTAX, tool=TOOL_NAME,
                    title=incorrect_number_of_sections.title, fields=fields, group=group,
                    text=incorrect_number_of_sections.text_template(**fields), report=report)


# TODO: IndentationError
# TODO: TabError