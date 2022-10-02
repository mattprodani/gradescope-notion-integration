import datetime
from time import mktime

class GSAssignment:
    """
    A class used to govern Gradescope assignments.
    Attributes
    ----------
    name : str
        the name of the assignment
    aid : str
        7-digit assignment id of the assignment
    course : GSCourse
        course object assignment is attached to
    status : str
        status of the assignment: submitted, submitted-late, no-submission, open, open-late
    open_date : str
        open date of the assignment
    close_date : str
        close date of the assignment
    points : tuple (float, float)
        tuple of points earned and total points
    regrades_on : bool
        bool of whether assignment is currently accepting regrade requests
    questions : list [str]
        list of questions in the assignment
    """

    def __init__(
        self,
        name: str,
        aid: str,
        course,
        status: str,
        open_date: str,
        close_date: str,
        url: str = None,
        points: tuple[float, float] = (0, 0),
        regrades_on: bool = False,
        questions: list[str] = None,
    ):
        """Create a GSAssignment object"""

        INVALID_ASSIGNMENT_ID = "0000000"
        self.name = name
        self.aid = aid
        self.gs_course = course
        self.course = course.name
        self.status = status
        self.open_date = datetime.datetime.strptime(open_date, "%Y-%m-%d %H:%M:%S %z")
        self.close_date = datetime.datetime.strptime(close_date, "%Y-%m-%d %H:%M:%S %z")
        self.current_date = datetime.datetime.now().astimezone()
        self.url = url
        self.time_left = (
            datetime.timedelta(0)
            if self.close_date < self.current_date
            else self.current_date - self.close_date
        )
        self.points = points
        self.regrades_on = regrades_on
        self.questions = questions

        if self.aid == INVALID_ASSIGNMENT_ID:
            self.aid = self._encode_self()


    def _encode_self(self):
        val = int(self.gs_course.cid)
        val += mktime(self.open_date.utctimetuple())
        val += mktime(self.close_date.utctimetuple())
        for c in self.name:
            val += ord(c)
        val %= 10000000
        return str(int(val))
        

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__[key] if key in self.__dict__ else default

    def __str__(self):
        return f"[#Assignment# {self.name} ({self.aid}) Course: {self.course} \t| Points: {self.points} \t {self.status}]"