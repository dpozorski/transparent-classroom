from enum import Enum


class ModelType(Enum):
    """
    Model Type Enum Class

    The available model endpoints provided by the Transparent Classroom API.

    Attributes:


    """

    """
    The model used for accessing teacher/staff activities with the learners. 
    
    """
    ACTIVITY = "activity"

    """
    The model used for user authentication.
    
    """
    AUTHENTICATION = "authenticate"

    """
    The model used to record attributes about the children/learners at the school.
    
    """
    CHILDREN = "children"

    """
    The model used to aggregate classrooms of students, staff, lesson sets, etc.
    
    """
    CLASSROOMS = "classrooms"

    """
    The model used for recording the details of learner conference reports created by staff.
    
    """
    CONFERENCE_REPORTS = "conference_reports"

    """
    The model used to record classroom/student events.
    
    """
    EVENTS = "events"

    """
    The model used to record Transparent Classroom form details.
    
    """
    FORMS = "forms"

    """
    The model used to record Transparent Classroom form template details.

    """
    FORM_TEMPLATES = "form_templates"

    """
    The model used to aggregate sets of lessons for a classroom. 
    
    """
    LESSON_SETS = "lesson_sets"

    """
    The model used to record learner proficiency in a given lesson/subject.
    
    """
    LEVELS = "levels"

    """
    The model used for applications to the school by families.
    
    """
    ONLINE_APPLICATIONS = "online_applications"

    """
    The model used for schools within a network of schools.
    
    """
    SCHOOLS = "schools"

    """
    The model used for school sessions/terms of classes.
    
    """
    SESSIONS = "sessions"

    """
    The model used authentication, roles, platform user details, etc.
    
    """
    USERS = "users"


class EndpointBehavior(Enum):
    """
    Endpoint Behavior Enum Class

    Attributes:


    """

    """
    Accept and Create Child (and Parent). Changes state of application to "Accepted", 
    creates a child, assigns child to classroom, and attaches application to child.

    """
    ACCEPT = "ACCEPT"

    """
    The endpoint will list the associated route objects.

    """
    LIST = "LIST"

    """
    The endpoint will show the object details.

    """
    SHOW = "SHOW"

    """
    The endpoint will show all records associated with a given object (the object
    reference is passed in as a parameter during the request).

    """
    SHOW_ALL = "SHOW_ALL"

    """
    The endpoint will show records filtered by some criteria.

    """
    SHOW_FILTERED = "SHOW_FILTERED"

    """
    Submit an application.

    """
    SUBMIT = "SUBMIT"

    """
    The endpoint will update a record.

    """
    UPDATE = "UPDATE"
