"""
Simple data classes for storing feedback to present to learners.
"""

__all__ = ['Feedback', 'FeedbackKind', 'FeedbackCategory',
           "AtomicFeedbackFunction", "CompositeFeedbackFunction",
           "FeedbackResponse"]

from pedal.core.location import Location
from pedal.core.report import MAIN_REPORT
from pedal.core.feedback_category import FeedbackKind, FeedbackCategory

PEDAL_DEVELOPERS = ["Austin Cory Bart <acbart@udel.edu>",
                    "Luke Gusukuma <lukesg08@vt.edu>"]


class Feedback:
    """
    A class for storing raw feedback.

    Attributes:
        label (str): An internal name for this specific piece of feedback. The
            label should be an underscore-separated string following the same
            conventions as names in Python. They do not have to be globally
            unique, but labels should be as unique as possible (especially
            within a category).
        tool (str, optional): An internal name for indicating the tool that created
            this feedback. Should be taken directly from the Tool itself. If `None`, then
            this was not created by a tool but directly by the control script.
        category (str): A human-presentable name showable to the learner, indicating what
            sort of feedback this falls into (e.g., "runtime", "syntax", "algorithm").
            More than one feedback will be in a category, but a feedback cannot be in
            more than one category.
        kind (str): The pedagogical role of this feedback, e.g., "misconception", "mistake",
            "hint", "constraint". Usually, a piece of Feedback is pointing out a mistake,
            but feedback can also be used for various other purposes.
        justification (str): An instructor-facing string briefly describing why this
            feedback was selected. Serves as a "TL;DR" for this feedback category, useful
            for debugging why a piece of feedback appeared.
        priority (str): An indication of how important this feedback is relative to other types
            of feedback in the same category. Might be "high/medium/low". Exactly how this
            gets used is up to the resolver, but typicaly it helps break ties.
        valence (int): Indicates whether this is negative, positive, or neutral feedback.
            Either 1, -1, or 0.

        title (str, optional): A formal, student-facing title for this feedback. If None, indicates
            that the :py:attr:`~pedal.core.feedback.Feedback.label` should be used instead.
        message (str): A markdown-formatted message (aka also supporting HTML) that could be rendered
            to the user.
        text (str): A console-friendly, plain-text message that could be rendered to the user.
        fields (Dict[str,Any]): The raw data that was used to interpolate the template to produce the message.
        location (:py:attr:`~pedal.core.location.Location` or list): Information about specific
            locations relevant to this message.

        score (int): A numeric score to modify the students' total score, indicating their overall performance.
            It is ultimately up to the Resolver to decide how to combine all the different scores; a typical
            strategy would be to add all the scores together for any non-muted feedback.
        correct (bool): Indicates that the entire submission should be considered correct (success) and that the
            task is now finished.
        muted (bool): Whether this piece of feedback is something that should be shown to a student. There are
            various use cases for muted feedback: they can serve as flags for later conditionals, suppressed
            default kinds of feedback, or perhaps feedback that is interesting for analysis but not pedagogically
            helpful to give to the student. They will still contribute to overall score, but not to the correcntess
            of the submission.
        unscored (bool): Whether or not this piece of feedback contributes to
            the score/correctness.

        author (List[str]): A list of names/emails that indicate who created this piece of feedback. They can be
            either names, emails, or combinations in the style of `"Cory Bart <acbart@udel.edu>"`.
        version (str): A version string in the style of Semantic Version (semvar) such as `"0.0.1"`. The last (third)
            digit should be incremented for small bug fixes/changes. The middle (second) digit should be used for more
            serious and intense changes. The first digit should be incremented when changes are made on exposure to
            learners or some other evidence-based motivation.
        tags (List[Tag]): Any tags that you want to attach to this feedback.

        group (int or str): Information about what logical grouping within the submission this belongs to. Various
            tools can chunk up a submission (e.g., by section), they can use this field to keep track of how that
            decision was made. Resolvers can also use this information to organize feedback or to report multiple
            categories.
        report (:py:class:`~pedal.core.report.Report`): The Report object to
            attach this feedback to. Defaults to MAIN_REPORT. Unspecified fields
            will be filled in by inspecting the current Feedback Function
            context.
    """

    POSITIVE_VALENCE = 1
    NEUTRAL_VALENCE = 0
    NEGATIVE_VALENCE = -1
    CATEGORIES = FeedbackCategory
    KINDS = FeedbackKind

    label = None
    category = None
    justification = None
    fields = None
    field_names = None
    kind = None
    title = None
    message = None
    text = None
    message_template = None
    text_template = None
    priority = None
    valence = None
    location = None
    score = None
    correct = None
    muted = None
    unscored = None
    tool = None
    version = '1.0.0'
    author = PEDAL_DEVELOPERS
    tags = None
    group = None

    def __init__(self, *args, label=None,
                 category=None, justification=None,
                 fields=None, field_names=None,
                 kind=None, title=None,
                 message=None, text=None,
                 message_template=None, text_template=None,
                 priority=None, valence=None,
                 location=None, score=None, correct=None,
                 muted=None, unscored=None,
                 tool=None, version=None, author=None,
                 tags=None,
                 group=None, report=MAIN_REPORT,
                 **kwargs):
        # Internal data
        self.report = report
        # Metadata
        if label is not None:
            self.label = label
        # Condition
        if category is not None:
            self.category = category
        if justification is not None:
            self.justification = justification
        # Response
        if kind is not None:
            self.kind = kind
        if priority is not None:
            self.priority = priority
        if valence is not None:
            self.valence = valence

        # Presentation
        if fields is not None:
            self.fields = fields
        else:
            self.fields = {}
        if field_names is not None:
            self.field_names = field_names
        if title is not None:
            self.title = title
        else:
            self.title = label
        if message is not None:
            self.message = message
        if text is not None:
            self.text = text
        if message_template is not None:
            self.message_template = message_template
        if text_template is not None:
            self.text_template = text_template

        # Locations
        if isinstance(location, int):
            location = [Location(location)]
        elif isinstance(location, Location):
            location = [location]
        # TODO: Handle tuples (Line, Col) and (Filename, Line, Col), and possibly lists thereof
        if location is not None:
            self.locations = location
        # Result
        if score is not None:
            self.score = score
        if correct is not None:
            self.correct = correct
        if muted is not None:
            self.muted = muted
        if unscored is not None:
            self.unscored = unscored
        # Metadata
        if tool is not None:
            self.tool = tool
        if version is not None:
            self.version = version
        if author is not None:
            self.author = author
        if tags is not None:
            self.tags = tags
        # Organizational
        if group is not None:
            self.group = group
        if self.field_names is not None:
            for field_name in self.field_names:
                self.fields[field_name] = kwargs.get(field_name)
        if 'location' not in self.fields and self.location is not None:
            self.fields['location'] = self.location
        # Self-attach to a given report?
        self._met_condition = self.condition(*args, **kwargs)
        # Generate the message and text fields as needed
        self.message = self._get_message()
        self.text = self._get_text()
        if report is not None and self._met_condition:
            report.add_feedback(self)

    def condition(self, *args, **kwargs):
        """
        Detect if this feedback is present in the code.
        Defaults to true.

        Returns:
            bool: Always returns True by default.
        """
        return True

    def _get_message(self):
        """
        Determines the appropriate value for the message. It will attempt
        to use this instance's message, but if it's not available then it will
        try to generate one from the message_template. Then, it falls back
        to _get_text.

        Returns:
            str: The message for this feedback.
        """
        if self.message is not None:
            return self.message
        if self.message_template is not None:
            return self.message_template.format(**self.fields)
        return self._get_text(False)

    def _get_text(self, fallback_to_message=True):
        """
        Determines the appropriate value for the plaintext response. It will
        attempt to use this instance's text, but if it's not available then it
        will try to generate one from the text_template. Then, it falls back
        to _get_message, unless the ``fallback_to_message`` parameter is False.

        Args:
            fallback_to_message (bool): Whether or not to try the message
                instead if there's no text available.

        Returns:
            str: The text for this feedback.
        """
        if self.text is not None:
            return self.text
        if self.text_template is not None:
            return self.text_template.format(**self.fields)
        if fallback_to_message:
            return self._get_message()
        else:
            # Simply no text to give!
            return ""

    def __bool__(self):
        return bool(self._met_condition)

    def __str__(self):
        """
        Create a string representation of this piece of Feedback for quick, dev purposes.
        Returns:
            str: String representation
        """
        return "<Feedback ({},{})>".format(self.category, self.label)

    def __repr__(self):
        """
        Create a string representation of this piece of Feedback that displays considerably more information.
        Returns:
            str: String representation with more data
        """
        metadata = ""
        if self.tool is not None:
            metadata += ", tool=" + self.tool
        if self.category is not None:
            metadata += ", category=" + self.category
        if self.priority is not None:
            metadata += ", priority=" + self.priority
        if self.group is not None:
            metadata += ", group=" + str(self.group)
        return "Feedback({}{})".format(self.label, metadata)


class FeedbackResponse(Feedback):
    """
    An extension of :py:class:`~pedal.core.feedback.Feedback` that is meant
    to indicate that the class should not have any condition behind its
    response.
    """


class AtomicFeedbackFunction(Feedback):
    """
    An extension of :py:class:`~pedal.core.feedback.Feedback` that is meant
    to indicate that the class should have a condition and response.
    """


def CompositeFeedbackFunction(*functions):
    """
    Decorator for functions that return multiple types of feedback functions.

    Args:
        functions (callable): A list of callable functions.

    Returns:
        callable: The decorated function.
    """
    def CompositeFeedbackFunction_with_attrs(function):
        """

        Args:
            function:

        Returns:

        """
        CompositeFeedbackFunction_with_attrs.functions = functions
        return function
    return CompositeFeedbackFunction_with_attrs
