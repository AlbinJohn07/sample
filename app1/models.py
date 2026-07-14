import re
import pandas as pd
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken


ROLE_CHOICES = [
    ('developer', 'Developer'),
    ('management', 'Management'),
    ('admin', 'Admin'),
    ('instructor', 'Instructor'),
    ('operator', 'Operator')
]

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, employeeid, first_name, last_name, role, hq, factory, department, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            employeeid=employeeid,
            first_name=first_name,
            last_name=last_name,
            role=role,
            hq=hq,
            factory=factory,
            department=department,
            is_active=True  
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, employeeid, first_name, last_name, role, hq, factory, department, password=None):
        user = self.create_user(
            email=email,
            employeeid=employeeid,
            first_name=first_name,
            last_name=last_name,
            role=role,
            hq=hq,
            factory=factory,
            department=department,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    employeeid = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='') 

    hq = models.CharField(max_length=50, blank=True, null=True)
    factory = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)

    status = models.BooleanField(default=True)  

    # Required Django Fields
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['employeeid', 'first_name', 'last_name', 'role', 'hq', 'factory', 'department']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }




from django.db import models
# Level Choices
LEVEL_CHOICES = [
    ('level_1', 'Level 1'),
    ('level_2', 'Level 2'),
    ('level_3', 'Level 3'),
    ('level_4', 'Level 4'),
]


class HQ(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Factory(models.Model):
    hq = models.ForeignKey(HQ, on_delete=models.CASCADE, related_name='factories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.hq.name})"


class Department(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.factory.name})"


class Line(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lines')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.department.name})"


class Level(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='levels')
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.get_name_display()} ({self.line.name})"






class Days(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='days')
    day = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.day} - {self.level.get_name_display()}"
    
















#@A0005
#@receiver(post_save, sender=User)
class EmployeeMaster(models.Model):
    pay_code = models.CharField(max_length=20, unique=True)
    card_no = models.CharField(max_length=20, unique=True)
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    birth_date = models.DateField()
    name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    desig_category = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField()
    auth_shift = models.CharField(max_length=50)
    shift_type = models.CharField(max_length=50)
    shift_pattern = models.CharField(max_length=50)
    first_weekly_off = models.CharField(max_length=10)
    second_weekly_off = models.CharField(max_length=10, blank=True, null=True)
    second_weekly_off_fh = models.CharField(max_length=10, blank=True, null=True)
    ot_allowed_rate = models.BooleanField(default=False)
    round_the_clock = models.BooleanField(default=False)
# this model is for employee master and updated 26/08/2025
    is_active = models.BooleanField(default=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    





# class Operator(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=50, unique=True)
#     date_of_joining = models.DateField()

#     def __str__(self):
#         return f"{self.name} ({self.code})"


# Top Level: Departments (like Production, Quality)
class MainDepartment(models.Model):
    name = models.CharField(max_length=100)  # Example: 'Production', 'Quality'

    def __str__(self):
        return self.name


# Second Level: Main Lines (like Weld Shop Line-1, Assembly Line-1)
class MainLine(models.Model):
    name = models.CharField(max_length=100)  # Example: 'Weld Shop Line-1 (Y17)'
    department = models.ForeignKey(MainDepartment, on_delete=models.CASCADE, related_name='main_lines')

    def __str__(self):
        return self.name


# Third Level: Sub Lines (like Bending Line, RSB Line)
class SubLine(models.Model):
    name = models.CharField(max_length=100)  # Example: 'Bending Line', 'FSB Line'
    main_line = models.ForeignKey(MainLine, on_delete=models.CASCADE, related_name='sub_lines')

    def __str__(self):
        return self.name



class Station(models.Model):
    sub_line = models.ForeignKey(SubLine, on_delete=models.CASCADE, related_name='stations',default='')
    station_number = models.IntegerField(unique=True)
    skill = models.CharField(max_length=100,default='')
    minimum_skill_required = models.CharField(max_length=100)
    min_operator_required = models.IntegerField()

    def __str__(self):
        return f" {self.skill}"


class OperatorSkill(models.Model):
    operator = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=100)
    sequence = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('operator', 'station')

    def __str__(self):
        return f"{self.operator} - {self.station} ({self.skill_level})"



class TrainingTopic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OperatorTraining(models.Model):
    operator = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    topic = models.ForeignKey(TrainingTopic, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('operator', 'topic')

    def __str__(self):
        return f"{self.operator} - {self.topic}"


class MonthlyAssignment(models.Model):
    operator = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=10)
    month = models.DateField()

    class Meta:
        unique_together = ('operator', 'station', 'month')

    def __str__(self):
        return f"{self.operator} assigned to {self.station} ({self.month})"
    





from django.db import models
from datetime import timedelta, date

class OperatorLevelTracking(models.Model):
    operator = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, related_name='level_trackings')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    day = models.PositiveIntegerField()  # e.g., Day 11, Day 15

    @property
    def milestone_date(self):
        if self.operator.joining_date:
            return self.operator.joining_date + timedelta(days=self.day)
        return None

    def is_today_milestone(self):
        return self.milestone_date == date.today()

    def __str__(self):
        return f"{self.operator.name} - {self.level.name} - Day {self.day}"







from django.db import models
from datetime import timedelta, date

class OperatorLevelEmailTracking(models.Model):
    operator = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, related_name='email_level_trackings')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    day = models.PositiveIntegerField()

    @property
    def milestone_date(self):
        if self.operator.joining_date:
            return self.operator.joining_date + timedelta(days=self.day)
        return None

    def is_today_milestone(self):
        return self.milestone_date == date.today()

    def __str__(self):
        return f"{self.operator.name} - {self.level.name} - Day {self.day}"


class TrackingEmail(models.Model):
    tracking = models.ForeignKey(OperatorLevelEmailTracking, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField()

    def __str__(self):
        return self.email









class Machine(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='machines/', null=True, blank=True)
    level = models.IntegerField()
    process = models.CharField(max_length=100, null=True, blank=True)  # Skill required
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name 
    



class MachineAllocationTrackingEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email




from django.core.exceptions import ValidationError

class MachineAllocation(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    allocated_at = models.DateTimeField(auto_now_add=True)
    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_STATUS_CHOICES,
        default='approved'
    )

    def __str__(self):
        return f"{self.machine.name} → {self.employee.name}"

    











class SkillTraining(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='skill_trainings')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.level.get_name_display()}"


class SubTopic(models.Model):
    skill_training = models.ForeignKey(SkillTraining, on_delete=models.CASCADE, related_name='subtopics')
    day = models.ForeignKey(Days, on_delete=models.CASCADE, related_name='subtopics')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SubTopicContent(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='subtopiccontents')
    title = models.CharField(max_length=100,default='')


class TrainingContent(models.Model):
    subtopic_content = models.ForeignKey(SubTopicContent, on_delete=models.CASCADE, related_name='contents',default='')
    description = models.TextField()
    training_file = models.FileField(upload_to='training_files/', blank=True, null=True)
    url_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Content for {self.subtopic_content.title}"
    



from django.db import models

class LevelTwoProduction(models.Model):
    name = models.CharField(max_length=100, default="Production")

    def __str__(self):
        return self.name


class LevelTwoLine(models.Model):
    name = models.CharField(max_length=100)
    production = models.ForeignKey(LevelTwoProduction, on_delete=models.CASCADE, related_name='leveltwolines')

    def __str__(self):
        return self.name
    

class LevelTwoSubStation(models.Model):
    name = models.CharField(max_length=100)
    line = models.ForeignKey(LevelTwoLine, on_delete=models.CASCADE, related_name='substations')

    def __str__(self):
        return self.name




class EmployeeLevelAssignment(models.Model):
    operator = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    line = models.ForeignKey(LevelTwoLine, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operator.name} assigned to {self.level}"

# ----- OJT MONITORING SHEET LEVEL 2 --------#

from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import transaction

class LevelTwoTraineeInfo(models.Model):
    traineeId = models.CharField(max_length=100)
    trainee_name = models.CharField(max_length=100)
    station = models.ForeignKey(LevelTwoSubStation, on_delete=models.SET_NULL, null=True, related_name='trainees')
    trainer_name = models.CharField(max_length=100)
    line = models.ForeignKey(LevelTwoLine, on_delete=models.SET_NULL, null=True, related_name='trainees')

    training_status = models.CharField(max_length=10, default='No Data')

    def __str__(self):
        return self.trainee_name

    def calculate_and_save_training_status(self):
        last_day = LevelTwoOJTDay.objects.order_by('-id').first()
        if not last_day:
            self.training_status = "No Data"
            self.save()
            return self.training_status

        total_topics = LevelTwoTrainingTopic.objects.count()
        expected_score = total_topics * 10

        actual_score = LevelTwoOJTScore.objects.filter(
            trainee=self, day=last_day
        ).aggregate(total=models.Sum('score'))['total'] or 0

        self.training_status = "Pass" if actual_score == expected_score else "Fail"
        self.save()

        # 🔹 Check if Score already exists and update skill
        if self.training_status == "Pass":
            self.update_operator_skill()

        return self.training_status

    @transaction.atomic
    def update_operator_skill(self):
        """Update OperatorSkill if trainee passed OJT and Score is also passed."""
        # Match traineeId with EmployeeMaster
        employee = EmployeeMaster.objects.filter(employee_id=self.traineeId).first()
        if not employee:
            return None

        # Check if there is a score with passed=True for the same station
        score = Score.objects.filter(
            employee=employee, passed=True, skill__id=self.station.id
        ).first()

        if score:
            # Update or create OperatorSkill record
            OperatorSkill.objects.update_or_create(
                operator=employee,
                station=score.skill,
                defaults={'skill_level': 'Level 2'}
            )
            return "Updated to Level 2"

        return None


        

class LevelTwoTrainingTopic(models.Model):
    sl_no = models.PositiveIntegerField()
    topic = models.CharField(max_length=255)
    date = models.CharField(max_length=255)

    def _str_(self):
        return f"{self.sl_no}. {self.topic}"


class LevelTwoOJTDay(models.Model):
    name = models.CharField(max_length=20)  

    def _str_(self):
        return self.name


class LevelTwoOJTScore(models.Model):
    trainee = models.ForeignKey(LevelTwoTraineeInfo, on_delete=models.CASCADE,related_name='ojtscores')
    topic = models.ForeignKey(LevelTwoTrainingTopic, on_delete=models.CASCADE)
    day = models.ForeignKey(LevelTwoOJTDay, on_delete=models.CASCADE)
    
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def _str_(self):
        return f"{self.trainee.trainee_name} | {self.day.name} | {self.topic.topic} | Score: {self.score}"
    





from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class LevelTwoQuality(models.Model):
    name = models.CharField(max_length=100, default="Quality")

    def _str_(self):
        return self.name


class LevelTwoQualityLine(models.Model):
    name = models.CharField(max_length=100)
    quality = models.ForeignKey(LevelTwoQuality, on_delete=models.CASCADE, related_name='leveltwolines')

    def _str_(self):
        return self.name


class LevelTwoQualitySubStation(models.Model):
    name = models.CharField(max_length=100)
    line = models.ForeignKey(LevelTwoQualityLine, on_delete=models.CASCADE, related_name='substations')

    def _str_(self):
        return self.name


class LevelTwoQATraineeInfo(models.Model):
    traineeId = models.CharField(max_length=100)
    trainee_name = models.CharField(max_length=100)
    station = models.ForeignKey(LevelTwoQualitySubStation, on_delete=models.SET_NULL, null=True, related_name='trainees')
    trainer_name = models.CharField(max_length=100)
    line = models.ForeignKey(LevelTwoQualityLine, on_delete=models.SET_NULL, null=True, related_name='trainees')

    training_status = models.CharField(max_length=10, default='No Data')

    def _str_(self):
        return self.trainee_name

    def calculate_and_save_training_status(self):
        last_day = LevelTwoQAOJTDay.objects.order_by('-id').first()
        if not last_day:
            self.training_status = "No Data"
            self.save()
            return self.training_status

        total_topics = LevelTwoQATrainingTopic.objects.count()
        expected_score = total_topics * 10

        actual_score = LevelTwoQAOJTScore.objects.filter(
            trainee=self, day=last_day
        ).aggregate(total=models.Sum('score'))['total'] or 0

        self.training_status = "Pass" if actual_score == expected_score else "Fail"
        self.save()
        return self.training_status


class LevelTwoQATrainingTopic(models.Model):
    sl_no = models.PositiveIntegerField()
    topic = models.CharField(max_length=255)
    date = models.CharField(max_length=25)

    def _str_(self):
        return f"{self.sl_no}. {self.topic}"


class LevelTwoQAOJTDay(models.Model):
    name = models.CharField(max_length=20)

    def _str_(self):
        return self.name


class LevelTwoQAOJTScore(models.Model):
    trainee = models.ForeignKey(LevelTwoQATraineeInfo, on_delete=models.CASCADE, related_name='ojtscores')
    topic = models.ForeignKey(LevelTwoQATrainingTopic, on_delete=models.CASCADE)
    day = models.ForeignKey(LevelTwoQAOJTDay, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def _str_(self):
        return f"{self.trainee.trainee_name} | {self.day.name} | {self.topic.topic} | Score: {self.score}"



















class LevelThreeProduction(models.Model):
    name = models.CharField(max_length=100, default="Production")

    def __str__(self):
        return self.name


class LevelThreeLine(models.Model):
    name = models.CharField(max_length=100)
    production = models.ForeignKey(LevelThreeProduction, on_delete=models.CASCADE, related_name='level_three_lines')

    def __str__(self):
        return self.name


class LevelThreeSubStation(models.Model):
    name = models.CharField(max_length=100)
    line = models.ForeignKey(LevelThreeLine, on_delete=models.CASCADE, related_name='level_three_substations')

    def __str__(self):
        return self.name











class LevelThreeTraineeInfo(models.Model):
    trainee_id = models.CharField(max_length=100, default='')
    trainee_name = models.CharField(max_length=100)
    station = models.ForeignKey(LevelThreeSubStation, on_delete=models.SET_NULL, null=True, related_name='levelthree_trainees')
    trainer_name = models.CharField(max_length=100)
    line = models.ForeignKey(LevelThreeLine, on_delete=models.SET_NULL, null=True, related_name='levelthree_trainees')

    training_status = models.CharField(max_length=10, default='No Data')

    def __str__(self):
        return self.trainee_name

    def calculate_and_save_training_status(self):
        training_days = LevelThreeOJTDay.objects.all().order_by('id')
        total_topics = LevelThreeTrainingTopic.objects.count()

        if not training_days.exists() or total_topics == 0:
            self.training_status = "No Data"
            self.save()
            return self.training_status

        for day in training_days:
            scores = LevelThreeOJTScore.objects.filter(trainee=self, day=day)

            # Check that trainee has a score for each topic
            if scores.count() != total_topics:
                self.training_status = "Fail"
                self.save()
                return self.training_status

            # Check that each score is exactly 10
            if not all(score.score == 10 for score in scores):
                self.training_status = "Fail"
                self.save()
                return self.training_status

        self.training_status = "Pass"
        self.save()
        return self.training_status
    


class LevelThreeTrainingTopic(models.Model):
    sl_no = models.PositiveIntegerField()
    topic = models.CharField(max_length=255)
    date = models.CharField(max_length=25)

    def str(self):
        return f"{self.sl_no}.{self.topic}"


class LevelThreeOJTDay(models.Model):
    name = models.CharField(max_length=20)  # Example: 'Day-19', 'Day-20'

    def _str_(self):
        return self.name



class LevelThreeOJTScore(models.Model):
    trainee = models.ForeignKey(LevelThreeTraineeInfo, on_delete=models.CASCADE, related_name='ojtscores')
    topic = models.ForeignKey(LevelThreeTrainingTopic, on_delete=models.CASCADE)
    day = models.ForeignKey(LevelThreeOJTDay, on_delete=models.CASCADE)
    
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def _str_(self):
        return f"{self.trainee.trainee_name} | {self.day.name} | {self.topic.topic} | Score: {self.score}"
    






# -----QA OJT MONITORING SHEET LEVEL 3 --------




  


















class LevelThreeQATrainingTopic(models.Model):
    sl_no = models.PositiveIntegerField()
    topic = models.CharField(max_length=255)
    date = models.CharField(max_length=25)

    def str(self):
        return f"{self.sl_no}.{self.topic}"


class LevelThreeQAOJTDay(models.Model):
    name = models.CharField(max_length=20)  

    def str(self):
        return self.name


class LevelThreeQuality(models.Model):
    name = models.CharField(max_length=100, default="QualityLevelThree")

    def _str_(self):
        return self.name


class LevelThreeQualityLine(models.Model):
    name = models.CharField(max_length=100)
    quality = models.ForeignKey(LevelThreeQuality, on_delete=models.CASCADE, related_name='qualitylevelthreelines')

    def _str_(self):
        return self.name

class LevelThreeQualitySubStation(models.Model):
    name = models.CharField(max_length=100)
    line = models.ForeignKey(
        LevelThreeQualityLine,   # ✅ Should be LevelThreeQualityLine, not LevelTwoQualityLine
        on_delete=models.CASCADE,
        related_name='levelthree_substations'  # ✅ unique name
    )

    def _str_(self):
        return self.name


class LevelThreeQATraineeInfo(models.Model):
    traineeId = models.CharField(max_length=100)
    trainee_name = models.CharField(max_length=100)
    trainer_name = models.CharField(max_length=100)
    line = models.ForeignKey(LevelThreeQualityLine, on_delete=models.SET_NULL, null=True, related_name='levelthreequalitytrainees')
    station = models.ForeignKey(LevelThreeQualitySubStation, on_delete=models.SET_NULL, null=True, related_name='trainees')

    training_status = models.CharField(max_length=10, default='No Data')

    def _str_(self):
        return self.trainee_name

    def calculate_and_save_training_status(self):
        training_days = LevelThreeQAOJTDay.objects.all().order_by('id')
        total_topics = LevelThreeQATrainingTopic.objects.count()

        if not training_days.exists() or total_topics == 0:
            self.training_status = "No Data"
            self.save()
            return self.training_status

        for day in training_days:
            scores = LevelThreeQAOJTScore.objects.filter(trainee=self, day=day)

            # Check that trainee has a score for each topic
            if scores.count() != total_topics:
                self.training_status = "Fail"
                self.save()
                return self.training_status

            # Check that each score is exactly 10
            if not all(score.score == 10 for score in scores):
                self.training_status = "Fail"
                self.save()
                return self.training_status

        self.training_status = "Pass"
        self.save()
        return self.training_status

        



from django.core.validators import MinValueValidator, MaxValueValidator

class LevelThreeQAOJTScore(models.Model):
    trainee = models.ForeignKey(LevelThreeQATraineeInfo, on_delete=models.CASCADE, related_name='ojtscores')
    topic = models.ForeignKey(LevelThreeQATrainingTopic, on_delete=models.CASCADE)
    day = models.ForeignKey(LevelThreeQAOJTDay, on_delete=models.CASCADE)

    
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def str(self):
        return f"{self.trainee.trainee_name} | {self.day.name} | {self.topic.topic} | Score: {self.score}"
    trainee = models.ForeignKey(LevelThreeQATraineeInfo, on_delete=models.CASCADE, related_name='ojtscores')
    topic = models.ForeignKey(LevelThreeQATrainingTopic, on_delete=models.CASCADE)
    day = models.ForeignKey(LevelThreeQAOJTDay, on_delete=models.CASCADE)

    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def str(self):
        return f"{self.trainee.trainee_name} | {self.day.name} | {self.topic.topic} | Score: {self.score}"
    from django.db import models

# class ARVRTrainingContent(models.Model):
#     description = models.TextField()
#     arvr_file = models.FileField(upload_to='arvr_files/', blank=True, null=True)

#     def __str__(self):
#         return f"AR/VR Content - {self.description[:30]}..."
class ARVRTrainingContent(models.Model):
    description = models.TextField()
    arvr_file = models.FileField(upload_to='arvr_files/', blank=True, null=True)
    url_link = models.TextField(max_length=500, blank=True, null=True)
    def __str__(self):
        return f"AR/VR Content - {self.description[:30]}..." 











from django.db import models
from django.core.exceptions import ValidationError

class MCQQuestion(models.Model):
    subtopic_content = models.ForeignKey(
        'SubTopicContent', on_delete=models.CASCADE, related_name='mcq_questions', null=True, blank=True
    )
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def _str_(self):
        return self.question

    def clean(self):
        if self.correct_answer not in [
            self.option_a, self.option_b, self.option_c, self.option_d
        ]:
            raise ValidationError("Correct answer must match one of the options.")







from django.db import models

from django.db import models

class BiometricAttendance(models.Model):
    sr_no = models.IntegerField(verbose_name="Sr.No.")
    pay_code = models.CharField(max_length=20, verbose_name="PayCode")
    card_no = models.CharField(max_length=20, verbose_name="Card No")
    employee_name = models.CharField(max_length=100, verbose_name="Employee Name")
    department = models.CharField(max_length=100, verbose_name="Department")
    designation = models.CharField(max_length=100, verbose_name="Designation")
    shift = models.CharField(max_length=10, verbose_name="Shift")
    start = models.TimeField(verbose_name="Start")
    in_time = models.TimeField(verbose_name="In")
    out_time = models.TimeField(verbose_name="Out")
    hrs_works = models.TimeField(null=True, blank=True, verbose_name="Hrs Works")
    status = models.CharField(max_length=10, verbose_name="Status")
    early_arrival = models.CharField(max_length=100, null=True, blank=True, verbose_name="Early Arriv.")
    late_arrival = models.CharField(max_length=100, null=True, blank=True, verbose_name="Late Arriv.")
    shift_early = models.CharField(max_length=100, null=True, blank=True, verbose_name="Shift Early")
    excess_lunch = models.CharField(max_length=100, null=True, blank=True, verbose_name="Excess Lunch")
    ot = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ot")
    ot_amount = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ot Amount")
    manual = models.CharField(max_length=100, null=True, blank=True, verbose_name="Manual")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('card_no', 'created_at')  # ensure one entry per card per upload date

    def __str__(self):
        return f"{self.employee_name} ({self.card_no}) on {self.created_at} - {self.status}"










from django.utils import timezone

from django.utils import timezone

from django.utils import timezone

class MultiSkilling(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('scheduled', 'Scheduled'),
        ('inprogress', 'In Progress'),
        ('rescheduled', 'Rescheduled'),
        ('completed', 'Completed'),
    ]

    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE,blank=True, null=True)
    skill_level = models.ForeignKey(Level, on_delete=models.CASCADE,blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')


    reason = models.TextField(blank=True, null=True)
    refreshment_date = models.DateField(blank=True, null=True)

    def _str_(self):
     return f"{self.skill} - Level {self.skill_level.skill_level if self.skill_level else 'N/A'}"


    def update_status_by_date(self):
        today = timezone.now().date()
        if today < self.start_date:
            self.status = 'scheduled'
        elif self.start_date <= today <= self.end_date:
            self.status = 'inprogress'
        elif today > self.end_date:
            self.status = 'completed'
        self.save()

    
class RefreshmentTraining(models.Model):
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='refreshment_trainings')
    skill = models.ForeignKey(MultiSkilling, on_delete=models.CASCADE)
    skill_level = models.ForeignKey(OperatorSkill, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason_for_refreshment = models.TextField(blank=True, null=True)

    @property
    def card_no(self):
        return self.employee.card_no






from django.db import models

class TrainingReport(models.Model):
    month = models.DateField()  # e.g., 2024-01-01 for January 2024
    new_operators_joined = models.PositiveIntegerField(default=0)
    new_operators_trained = models.PositiveIntegerField(default=0)
    total_trainings_planned = models.PositiveIntegerField(default=0)
    total_trainings_actual = models.PositiveIntegerField(default=0)

    def _str_(self):
        return f"{self.month.strftime('%B %Y')} - Joined: {self.new_operators_joined}, Trained: {self.new_operators_trained}"






from django.db import models

class UnifiedDefectReport(models.Model):
    CATEGORY_CHOICES = [
        ('MSIL', 'MSIL'),
        ('Tier-1', 'Tier-1'),
        ('All Plants', 'All Plants'),
        ('CTQ', 'CTQ'),
    ]

    month = models.DateField()  # First day of the month
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    # Defect data
    total_defects = models.PositiveIntegerField(default=0)
    ctq_defects = models.PositiveIntegerField(default=0)

    # Internal rejection data (optional if category is 'Internal')
    total_internal_rejection = models.PositiveIntegerField(default=0)
    ctq_internal_rejection = models.PositiveIntegerField(default=0)

    # Tier-1 specific defect data
    tier1_total_defects = models.PositiveIntegerField(default=0)
    tier1_ctq_defects = models.PositiveIntegerField(default=0)

    def _str_(self):
        return (
            f"{self.category} - {self.month.strftime('%B %Y')} | "
            f"Total: {self.total_defects}, CTQ: {self.ctq_defects}, "
            f"Internal: {self.total_internal_rejection}, CTQ Internal: {self.ctq_internal_rejection}, "
            f"Tier-1 Total: {self.tier1_total_defects}, Tier-1 CTQ: {self.tier1_ctq_defects}"
        )
    

#test part integration

from django.db import models

class KeyEvent(models.Model):
    base_id = models.IntegerField()
    key_id = models.IntegerField()
    key_sn = models.CharField(max_length=255, default='unknown')
    mode = models.IntegerField()
    timestamp = models.DateTimeField()
    info = models.CharField(max_length=255)
    client_timestamp = models.DateTimeField()
    event_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class ConnectEvent(models.Model):
    base_id = models.IntegerField()
    mode = models.IntegerField()
    info = models.CharField(max_length=255)
    timestamp = models.DateTimeField()




class VoteEvent(models.Model):
    base_id = models.IntegerField()
    mode = models.IntegerField()
    info = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

# dynamic quesitions 

# models.py

class QuestionPaper(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_index = models.IntegerField(choices=[(i, chr(65+i)) for i in range(4)])

    def __str__(self):
        return self.question_text

    def get_options(self):
        return [self.option_a, self.option_b, self.option_c, self.option_d]


class TestSession(models.Model):
    test_name = models.CharField(max_length=100)  # ← Make sure this exists
    key_id = models.CharField(max_length=10)
    employee = models.ForeignKey('EmployeeMaster', on_delete=models.CASCADE)
    level = models.CharField(max_length=100, null=True)  # 🆕
    skill = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, blank=True)
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, related_name='test_sessions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('test_name', 'key_id')

    def __str__(self):
        return f"{self.test_name} - {self.key_id} ({self.employee.name})"



# models.py
class Score(models.Model):
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    marks = models.IntegerField()
    test_name = models.CharField(max_length=100, blank=True)
    test = models.ForeignKey(TestSession, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    percentage = models.FloatField(default=0)
    passed = models.BooleanField(default=False)
    level = models.CharField(max_length=100, null=True, blank=True)
    skill = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, blank=True)


 

    def save(self, *args, **kwargs):
     super().save(*args, **kwargs)

     if self.passed:
        trainee = LevelTwoTraineeInfo.objects.filter(traineeId=self.employee.employee_id).first()
        if trainee and trainee.training_status == "Pass":
            trainee.update_operator_skill()






# class HanContent(models.Model):
#     title = models.CharField(max_length=100, default='')

#     def _str_(self):
#         return self.title


# class HanTrainingContent(models.Model):
#     han_content = models.ForeignKey(HanContent, on_delete=models.CASCADE, related_name='contents')
#     description = models.TextField()
#     training_file = models.FileField(upload_to='training_files/', blank=True, null=True)
#     url_link = models.URLField(max_length=500, blank=True, null=True)

#     def _str_(self):
#         return f"Training Content for {self.han_content.title}"
    

# class ShoContent(models.Model):
#     title = models.CharField(max_length=100, default='')

#     def _str_(self):
#         return self.title


# class ShoTrainingContent(models.Model):
#     sho_content = models.ForeignKey(ShoContent, on_delete=models.CASCADE, related_name='contents', default='')
#     description = models.TextField()
#     training_file = models.FileField(upload_to='training_files/', blank=True, null=True)
#     url_link = models.URLField(max_length=500, blank=True, null=True)

#     def _str_(self):
#         return f"Content for {self.sho_content.title}"




class ManagementReview(models.Model):
    month_year = models.DateField()
    new_operators_joined = models.IntegerField()
    new_operators_trained = models.IntegerField()
    total_training_plans = models.IntegerField()
    total_trainings_actual = models.IntegerField()
    total_defects_msil = models.IntegerField()
    ctq_defects_msil = models.IntegerField()
    total_defects_tier1 = models.IntegerField()
    ctq_defects_tier1 = models.IntegerField()
    total_internal_rejection = models.IntegerField()
    ctq_internal_rejection = models.IntegerField()

    def _str_(self):
        return self.month_year.strftime('%b %y')
    


from django.db import models

class CompanyLogo(models.Model):
    name = models.CharField(max_length=100)  # Optional: Name of the logo (e.g., company name)
    logo = models.ImageField(upload_to='logos/',blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.name or f"Logo {self.id}"
    

class AdvancedManpowerCTQ(models.Model):
    month_year_ctq = models.DateField()
    total_stations_ctq = models.IntegerField()
    operator_required_ctq = models.IntegerField()
    operator_availability_ctq = models.IntegerField()
    buffer_manpower_required_ctq = models.IntegerField()
    buffer_manpower_availability_ctq = models.IntegerField()
    attrition_trend_ctq = models.IntegerField()
    absentee_trend_ctq = models.IntegerField()
    planned_units_ctq = models.IntegerField()
    actual_production_ctq = models.IntegerField()
    

    # New relations
    factory = models.ForeignKey('Factory', on_delete=models.CASCADE, related_name='ctq_records', null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='ctq_records', null=True, blank=True)

    def _str_(self):
        return f"{self.month_year_ctq.strftime('%b %y')} - {self.factory.name} - {self.department.name}"



class OperatorRequirement(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='operator_requirements')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='operator_requirements')
    month = models.DateField(help_text="Any date in the month (used for month tracking)")
    level = models.IntegerField(help_text="Skill level or grade")
    operator_required = models.PositiveIntegerField()
    operator_available = models.PositiveIntegerField()

    def _str_(self):
        return f"{self.factory.name} - {self.department.name} | Level {self.level} - {self.month.strftime('%B %Y')}"
    


from django.db import models

class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')  # stores in MEDIA_ROOT/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title










class TrainingBatch(models.Model):
    """ Manages the state of a training batch. """
    batch_id = models.CharField(max_length=20, unique=True, primary_key=True, help_text="e.g., BATCH-070824")
    is_active = models.BooleanField(default=True, help_text="Active batches appear in the attendance dropdown.")
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def _str_(self):
        return self.batch_id



# your_app/models.py
import uuid
from django.db import models
from datetime import datetime
# Assuming TrainingBatch is defined in this file too
# from .models import TrainingBatch 

class UserInfo(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(
        max_length=50,
        help_text="User's first name",
        null=True,
        blank=True
    )
    temp_id = models.CharField(
        max_length=50,
        unique=True,
        editable=True,
        help_text="Auto-generated temporary ID for the user"
    )
    
    # --- THIS IS THE MISSING LINE ---
    batch_id = models.CharField(
        max_length=20, 
        editable=False, 
        null=True, # Allow null for existing records
        blank=True
    )
    # --------------------------------

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        help_text="User's email address (optional)"
    )
    phone_number = models.CharField(
        max_length=17,
        help_text="User's phone number (required)"
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default='M',
        help_text="User's sex"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Information"
        verbose_name_plural = "User Information"

    def _str_(self):
        return f"{self.first_name} ({self.temp_id})"

    def save(self, *args, **kwargs):
        if not self.temp_id:
            self.temp_id = f"TEMP{uuid.uuid4().hex[:12].upper()}"
            
        # This part now works because the field exists
        if not self.pk:
            today = datetime.now().strftime("%d%m%y")
            self.batch_id = f"BATCH-{today}"
            TrainingBatch.objects.get_or_create(batch_id=self.batch_id)
            
        super().save(*args, **kwargs)



class TrainingAttendance(models.Model):
    """ Stores daily attendance for each user in a batch. """
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='attendances')
    batch = models.ForeignKey(TrainingBatch, on_delete=models.CASCADE, related_name='attendances', to_field='batch_id')
    day_number = models.PositiveIntegerField(help_text="Training day number (1-6)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    # --- NEW FIELD ---
    # This field will store the actual calendar date the attendance was marked on.
    attendance_date = models.DateField(help_text="The calendar date this attendance was recorded" ,null=True, blank= True)
    
    date_marked = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['batch', 'user', 'day_number']
        # A user can only have one attendance status per day in a given batch.
        unique_together = ('user', 'batch', 'day_number')

    def _str_(self):
        return f"{self.user.first_name} - {self.batch.batch_id} - Day {self.day_number}: {self.status}"


class HumanBodyCheck(models.Model):
    STATUS_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('pending', 'Pending'),
    ]

    temp_id = models.CharField(max_length=50)  # Temporary ID from the user
    check_date = models.DateTimeField(auto_now_add=True)
    overall_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')

    # Physical Fitness Checks
    color_vision = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    eye_movement = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    fingers_functionality = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    hand_deformity = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    joint_mobility = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    hearing = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    bending_ability = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')

    # Additional custom checks (stored as JSON)
    additional_checks = models.JSONField(default=list, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-check_date']
        verbose_name = 'Human Body Check'
        verbose_name_plural = 'Human Body Checks'

    def save(self, *args, **kwargs):
        # Calculate overall status before saving
        checks = [
            self.color_vision,
            self.eye_movement,
            self.fingers_functionality,
            self.hand_deformity,
            self.joint_mobility,
            self.hearing,
            self.bending_ability
        ]

        # Check additional checks
        for check in self.additional_checks:
            checks.append(check.get('status', 'pending'))

        if 'fail' in checks:
            self.overall_status = 'fail'
        elif all(status == 'pass' for status in checks):
            self.overall_status = 'pass'
        else:
            self.overall_status = 'pending'

        super().save(*args, **kwargs)

    def _str_(self):
        return f"Check for {self.temp_id} - {self.get_overall_status_display()}"



class SDCOrientationFeedback(models.Model):
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE,
                             related_name='orientation_feedbacks', default='')

    pay_code = models.CharField(max_length=20, unique=True, default='')
    card_no = models.CharField(max_length=20, unique=True, default='')
    sex = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female')],
        default=''
    )
    birth_date = models.DateField()
    guardian_name = models.CharField(max_length=100, default='')
    department = models.CharField(max_length=100, default='')
    section = models.CharField(max_length=100, default='')
    desig_category = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField(default='2025-08-05')

    def _str_(self):
        return f" ({self.pay_code})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save feedback first

        # Create or update EmployeeMaster
        from .models import EmployeeMaster  # Import inside to avoid circular import

        EmployeeMaster.objects.update_or_create(
            pay_code=self.pay_code,
            defaults={
                "card_no": self.card_no,
                "sex": self.sex,
                "birth_date": self.birth_date,
                "name": self.user.first_name,  # taking from UserInfo
                "guardian_name": self.guardian_name,
                "department": self.department,
                "section": self.section,
                "desig_category": self.desig_category,
                "joining_date": self.joining_date,
                # set defaults for required fields
                "auth_shift": "General",
                "shift_type": "Day",
                "shift_pattern": "Fixed",
                "first_weekly_off": "Sunday",
                "ot_allowed_rate": False,
                "round_the_clock": False,
            }
        )











# refresher training



class Training_category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Curriculum(models.Model):
    category = models.ForeignKey(
        Training_category, on_delete=models.CASCADE, related_name='topics')
    topic = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("category", "topic")
        ordering = ["topic"]

    def __str__(self):
        return f"{self.category.name} > {self.topic}"


class CurriculumContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('document', 'Document'),
        ('image', 'Image'),
        ('link', 'Link'),
    ]

    curriculum = models.ForeignKey(
        'Curriculum', on_delete=models.CASCADE, related_name='contents')
    content_name = models.CharField(max_length=200)
    content_type = models.CharField(
        max_length=10, choices=CONTENT_TYPE_CHOICES)

    file = models.FileField(
        upload_to='training_contents/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content_name


class Trainer_name(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Venues(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]

    training_category = models.ForeignKey(
        Training_category, on_delete=models.CASCADE, related_name='scheduled_categories')
    training_name = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name='scheduled_topics')

    trainer = models.ForeignKey(
        Trainer_name, on_delete=models.SET_NULL, null=True)
    venue = models.ForeignKey(Venues, on_delete=models.SET_NULL, null=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    date = models.DateField()
    time = models.TimeField()

    employees = models.ManyToManyField(
        "EmployeeMaster", related_name='schedules')

    def __str__(self):
        return f"{self.training_name.topic} on {self.date}"


class EmployeeAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('rescheduled', 'Rescheduled'),
    ]

    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name='attendances')
    employee = models.ForeignKey(
        'EmployeeMaster', on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='present')
    notes = models.TextField(blank=True, null=True)

    # For rescheduling
    reschedule_date = models.DateField(blank=True, null=True)
    reschedule_time = models.TimeField(blank=True, null=True)
    reschedule_reason = models.TextField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('schedule', 'employee')

    def __str__(self):
        return f"{self.employee} - {self.schedule} - {self.status}"


class RescheduleLog(models.Model):
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name='reschedule_logs')
    employee = models.ForeignKey(
        'EmployeeMaster', on_delete=models.CASCADE, related_name='reschedule_logs')
    original_date = models.DateField()
    original_time = models.TimeField()
    new_date = models.DateField()
    new_time = models.TimeField()
    reason = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reschedule for {self.employee} on {self.schedule}"








# # multiskilling
from django.utils import timezone

class NewMultiSkilling(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('scheduled', 'Scheduled'),
        ('inprogress', 'In Progress'),
        ('rescheduled', 'Rescheduled'),
        ('completed', 'Completed'),
    ]

    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    operation = models.ForeignKey(
        Station, on_delete=models.CASCADE, null=True, blank=True)
    skill_level = models.ForeignKey(Level, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def save(self, *args, **kwargs):
        today = timezone.localdate()

        # Check if employee already has this skill at the same station
        from .models import OperatorSkill  # avoid circular import issues
        has_skill = OperatorSkill.objects.filter(
            operator=self.employee,
            station=self.operation,
            skill_level=self.skill_level.name  # since skill_level is FK, compare with name
        ).exists()

        if has_skill:
            self.status = "active"
        elif self.start_date:
            if self.start_date > today:
                self.status = "scheduled"
            elif self.start_date == today:
                self.status = "inprogress"
            else:
                self.status = "completed"  # optional

        super().save(*args, **kwargs)     



# hanchou and shokuchou 




class HanContent(models.Model):
    title = models.CharField(max_length=100, default='')

    def _str_(self):
        return self.title


# --- NEW MODEL ---
# This is the "Subtopic" that will live under a HanContent.
class HanSubtopic(models.Model):
    title = models.CharField(max_length=150)
    # This links each subtopic to its parent main topic.
    han_content = models.ForeignKey(HanContent, on_delete=models.CASCADE, related_name='subtopics')

    def __str__(self):
        # e.g., "Introduction to Python -> Week 1: Variables"
        return f"{self.han_content.title} -> {self.title}"



class HanTrainingContent(models.Model):
    # This ForeignKey has been CHANGED to point to HanSubtopic.
    han_subtopic = models.ForeignKey(HanSubtopic, on_delete=models.CASCADE, related_name='materials',  null=True)
    description = models.TextField()
    training_file = models.FileField(upload_to='training_files/', blank=True, null=True)
    url_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Material for {self.han_subtopic.title}"
    

    
class ShoContent(models.Model):
    title = models.CharField(max_length=100, default='')

    def _str_(self):
        return self.title



class ShoSubtopic(models.Model):
    title = models.CharField(max_length=150)
    # This links each subtopic to its parent main topic.
    sho_content = models.ForeignKey(ShoContent, on_delete=models.CASCADE, related_name='sho_subtopics')

    def __str__(self):
        # e.g., "Introduction to Python -> Week 1: Variables"
        return f"{self.sho_content.title} -> {self.title}"



class ShoTrainingContent(models.Model):
    sho_subtopic = models.ForeignKey(ShoSubtopic, on_delete=models.CASCADE, related_name='sho_materials',  null=True)
    sho_description = models.TextField()
    training_file = models.FileField(upload_to='training_files/', blank=True, null=True)
    url_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Material for {self.sho_subtopic.title}"




from django.db import models
from django.core.exceptions import ValidationError

class HanchouExamQuestion(models.Model):
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question[:50]  # show first 50 chars

    def clean(self):
        if self.correct_answer not in [
            self.option_a, self.option_b, self.option_c, self.option_d
        ]:
            raise ValidationError("Correct answer must match one of the options.")

from django.db.models import F, Q

class HanchouExamResult(models.Model):
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.PROTECT, related_name="hanchou_results")
    exam_name = models.CharField(max_length=50, default="hanchou", editable=False)
    started_at = models.DateTimeField()
    submitted_at = models.DateTimeField()
    total_questions = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    pass_mark_percent = models.PositiveSmallIntegerField(default=70)
    passed = models.BooleanField(default=False)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(score__lte=F("total_questions")),
                                   name="score_lte_total_questions"),
        ]

    @property
    def percentage(self):
        return 0 if not self.total_questions else round((self.score / self.total_questions) * 100, 2)

    def save(self, *args, **kwargs):
        self.passed = self.percentage >= self.pass_mark_percent
        super().save(*args, **kwargs)


from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q



class ShokuchouExamQuestion(models.Model):
    sho_question = models.TextField()
    sho_option_a = models.CharField(max_length=255)
    sho_option_b = models.CharField(max_length=255)
    sho_option_c = models.CharField(max_length=255)
    sho_option_d = models.CharField(max_length=255)
    sho_correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.sho_question[:50]  # show first 50 chars

    def clean(self):
        if self.sho_correct_answer not in [
            self.sho_option_a,
            self.sho_option_b,
            self.sho_option_c,
            self.sho_option_d,
        ]:
            raise ValidationError("Correct answer must match one of the options.")


class ShokuchouExamResult(models.Model):
    employee = models.ForeignKey(
        EmployeeMaster, on_delete=models.PROTECT, related_name="shokuchou_results"
    )
    sho_exam_name = models.CharField(max_length=50, default="shokuchou", editable=False)
    sho_started_at = models.DateTimeField()
    sho_submitted_at = models.DateTimeField()
    sho_total_questions = models.PositiveIntegerField()
    sho_score = models.PositiveIntegerField()
    sho_duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    sho_pass_mark_percent = models.PositiveSmallIntegerField(default=70)
    sho_passed = models.BooleanField(default=False)
    sho_remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(sho_score__lte=F("sho_total_questions")),
                name="sho_score_lte_total_questions",
            ),
        ]

    @property
    def sho_percentage(self):
        return (
            0
            if not self.sho_total_questions
            else round((self.sho_score / self.sho_total_questions) * 100, 2)
        )

    def save(self, *args, **kwargs):
        self.sho_passed = self.sho_percentage >= self.sho_pass_mark_percent
        super().save(*args, **kwargs)








class NewFactory(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name


class NewDepartment(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name


class NewLine(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name


class NewWorkstation(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name

















from django.db import models

class FactoryStructure(models.Model):
    factory_name = models.CharField(max_length=100)  # Renamed from 'name'

    def str(self):
        return self.factory_name


class ShopFloor(models.Model):
    factory_structure = models.ForeignKey(FactoryStructure, on_delete=models.CASCADE, related_name='shop_floors')
    shopfloor_name = models.CharField(max_length=100)  # Renamed from 'name'

    def str(self):
        return f"{self.shopfloor_name} ({self.factory_structure.factory_name})"


class LineStructure(models.Model):
    shop_floor = models.ForeignKey(ShopFloor, on_delete=models.CASCADE, related_name='lines')
    line_name = models.CharField(max_length=100)  # Renamed from 'name'

    def str(self):
        return f"{self.line_name} ({self.shop_floor.shopfloor_name})"


class StationStructure(models.Model):
    line = models.ForeignKey(LineStructure, on_delete=models.CASCADE, related_name='stations')
    station_name = models.CharField(max_length=100)  # Renamed from 'name'

    def str(self):
        return f"{self.station_name} ({self.line.line_name})"













# class ProductionPlan(models.Model):
#     month = models.CharField(max_length=20)
#     year = models.PositiveIntegerField()

#     factory = models.ForeignKey(FactoryStructure, on_delete=models.CASCADE)
#     shop_floor = models.ForeignKey(ShopFloor, on_delete=models.CASCADE, null=True, blank=True)
#     line = models.ForeignKey(LineStructure, on_delete=models.CASCADE, null=True, blank=True)
#     station = models.ForeignKey(StationStructure, on_delete=models.CASCADE, null=True, blank=True)

#     total_production_plan = models.PositiveIntegerField()
#     # New: Actual number of units for the month
#     total_production_actual = models.PositiveIntegerField(default=0)

#     # New: Total operators required (Plan and Actual)
#     total_operators_required_plan = models.PositiveIntegerField(default=0)
#     total_operators_required_actual = models.PositiveIntegerField(default=0)

#     # CTQ Plan
#     ctq_plan_l1 = models.PositiveIntegerField('CTQ Plan L1', default=0)
#     ctq_plan_l2 = models.PositiveIntegerField('CTQ Plan L2', default=0)
#     ctq_plan_l3 = models.PositiveIntegerField('CTQ Plan L3', default=0)
#     ctq_plan_l4 = models.PositiveIntegerField('CTQ Plan L4', default=0)
#     ctq_plan_total = models.PositiveIntegerField('CTQ Plan Total', default=0)
    
#     # CTQ Actual
#     ctq_actual_l1 = models.PositiveIntegerField('CTQ Actual L1', default=0)
#     ctq_actual_l2 = models.PositiveIntegerField('CTQ Actual L2', default=0)
#     ctq_actual_l3 = models.PositiveIntegerField('CTQ Actual L3', default=0)
#     ctq_actual_l4 = models.PositiveIntegerField('CTQ Actual L4', default=0)
#     ctq_actual_total = models.PositiveIntegerField('CTQ Actual Total', default=0)

#     # PDI Plan
#     pdi_plan_l1 = models.PositiveIntegerField('PDI Plan L1', default=0)
#     pdi_plan_l2 = models.PositiveIntegerField('PDI Plan L2', default=0)
#     pdi_plan_l3 = models.PositiveIntegerField('PDI Plan L3', default=0)
#     pdi_plan_l4 = models.PositiveIntegerField('PDI Plan L4', default=0)
#     pdi_plan_total = models.PositiveIntegerField('PDI Plan Total', default=0)
    
#     # PDI Actual
#     pdi_actual_l1 = models.PositiveIntegerField('PDI Actual L1', default=0)
#     pdi_actual_l2 = models.PositiveIntegerField('PDI Actual L2', default=0)
#     pdi_actual_l3 = models.PositiveIntegerField('PDI Actual L3', default=0)
#     pdi_actual_l4 = models.PositiveIntegerField('PDI Actual L4', default=0)
#     pdi_actual_total = models.PositiveIntegerField('PDI Actual Total', default=0)

#     # OTHER Plan
#     other_plan_l1 = models.PositiveIntegerField('Other Plan L1', default=0)
#     other_plan_l2 = models.PositiveIntegerField('Other Plan L2', default=0)
#     other_plan_l3 = models.PositiveIntegerField('Other Plan L3', default=0)
#     other_plan_l4 = models.PositiveIntegerField('Other Plan L4', default=0)
#     other_plan_total = models.PositiveIntegerField('Other Plan Total', default=0)
    
#     # OTHER Actual
#     other_actual_l1 = models.PositiveIntegerField('Other Actual L1', default=0)
#     other_actual_l2 = models.PositiveIntegerField('Other Actual L2', default=0)
#     other_actual_l3 = models.PositiveIntegerField('Other Actual L3', default=0)
#     other_actual_l4 = models.PositiveIntegerField('Other Actual L4', default=0)
#     other_actual_total = models.PositiveIntegerField('Other Actual Total', default=0)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def str(self):
#         return f"{self.month} {self.year} - {self.factory.factory_name} - {self.line.line_name}"
    


class ProductionPlan(models.Model):
    month = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    factory = models.ForeignKey(FactoryStructure, on_delete=models.CASCADE)
    shop_floor = models.ForeignKey(ShopFloor, on_delete=models.CASCADE, null=True, blank=True)
    line = models.ForeignKey(LineStructure, on_delete=models.CASCADE, null=True, blank=True)
    station = models.ForeignKey(StationStructure, on_delete=models.CASCADE, null=True, blank=True)

    total_production_plan = models.PositiveIntegerField()
    total_production_actual = models.PositiveIntegerField(default=0)

    total_operators_required_plan = models.PositiveIntegerField(default=0)
    total_operators_required_actual = models.PositiveIntegerField(default=0)

    attrition_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0,
        help_text="Attrition rate in percentage"
    )

  # CTQ Plan
    ctq_plan_l1 = models.PositiveIntegerField('CTQ Plan L1', default=0)
    ctq_plan_l2 = models.PositiveIntegerField('CTQ Plan L2', default=0)
    ctq_plan_l3 = models.PositiveIntegerField('CTQ Plan L3', default=0)
    ctq_plan_l4 = models.PositiveIntegerField('CTQ Plan L4', default=0)
    ctq_plan_total = models.PositiveIntegerField('CTQ Plan Total', default=0)
    
    # CTQ Actual
    ctq_actual_l1 = models.PositiveIntegerField('CTQ Actual L1', default=0)
    ctq_actual_l2 = models.PositiveIntegerField('CTQ Actual L2', default=0)
    ctq_actual_l3 = models.PositiveIntegerField('CTQ Actual L3', default=0)
    ctq_actual_l4 = models.PositiveIntegerField('CTQ Actual L4', default=0)
    ctq_actual_total = models.PositiveIntegerField('CTQ Actual Total', default=0)

    # PDI Plan
    pdi_plan_l1 = models.PositiveIntegerField('PDI Plan L1', default=0)
    pdi_plan_l2 = models.PositiveIntegerField('PDI Plan L2', default=0)
    pdi_plan_l3 = models.PositiveIntegerField('PDI Plan L3', default=0)
    pdi_plan_l4 = models.PositiveIntegerField('PDI Plan L4', default=0)
    pdi_plan_total = models.PositiveIntegerField('PDI Plan Total', default=0)
    
    # PDI Actual
    pdi_actual_l1 = models.PositiveIntegerField('PDI Actual L1', default=0)
    pdi_actual_l2 = models.PositiveIntegerField('PDI Actual L2', default=0)
    pdi_actual_l3 = models.PositiveIntegerField('PDI Actual L3', default=0)
    pdi_actual_l4 = models.PositiveIntegerField('PDI Actual L4', default=0)
    pdi_actual_total = models.PositiveIntegerField('PDI Actual Total', default=0)

    # OTHER Plan
    other_plan_l1 = models.PositiveIntegerField('Other Plan L1', default=0)
    other_plan_l2 = models.PositiveIntegerField('Other Plan L2', default=0)
    other_plan_l3 = models.PositiveIntegerField('Other Plan L3', default=0)
    other_plan_l4 = models.PositiveIntegerField('Other Plan L4', default=0)
    other_plan_total = models.PositiveIntegerField('Other Plan Total', default=0)
    
    # OTHER Actual
    other_actual_l1 = models.PositiveIntegerField('Other Actual L1', default=0)
    other_actual_l2 = models.PositiveIntegerField('Other Actual L2', default=0)
    other_actual_l3 = models.PositiveIntegerField('Other Actual L3', default=0)
    other_actual_l4 = models.PositiveIntegerField('Other Actual L4', default=0)
    other_actual_total = models.PositiveIntegerField('Other Actual Total', default=0) 

    # --- Bifurcation ---
    bifurcation_plan_l1 = models.PositiveIntegerField(default=0)
    bifurcation_plan_l2 = models.PositiveIntegerField(default=0)
    bifurcation_plan_l3 = models.PositiveIntegerField(default=0)
    bifurcation_plan_l4 = models.PositiveIntegerField(default=0)

    bifurcation_actual_l1 = models.PositiveIntegerField(default=0)
    bifurcation_actual_l2 = models.PositiveIntegerField(default=0)
    bifurcation_actual_l3 = models.PositiveIntegerField(default=0)
    bifurcation_actual_l4 = models.PositiveIntegerField(default=0)

    # --- New Fields for clarity ---
    grand_total_plan = models.PositiveIntegerField(default=0)
    grand_total_actual = models.PositiveIntegerField(default=0)
    gap_plan = models.IntegerField(default=0)
    gap_actual = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Totals (same as your current logic)...
        self.ctq_plan_total = (self.ctq_plan_l1 or 0) + (self.ctq_plan_l2 or 0) + (self.ctq_plan_l3 or 0) + (self.ctq_plan_l4 or 0)
        self.ctq_actual_total = (self.ctq_actual_l1 or 0) + (self.ctq_actual_l2 or 0) + (self.ctq_actual_l3 or 0) + (self.ctq_actual_l4 or 0)

        self.pdi_plan_total = (self.pdi_plan_l1 or 0) + (self.pdi_plan_l2 or 0) + (self.pdi_plan_l3 or 0) + (self.pdi_plan_l4 or 0)
        self.pdi_actual_total = (self.pdi_actual_l1 or 0) + (self.pdi_actual_l2 or 0) + (self.pdi_actual_l3 or 0) + (self.pdi_actual_l4 or 0)

        self.other_plan_total = (self.other_plan_l1 or 0) + (self.other_plan_l2 or 0) + (self.other_plan_l3 or 0) + (self.other_plan_l4 or 0)
        self.other_actual_total = (self.other_actual_l1 or 0) + (self.other_actual_l2 or 0) + (self.other_actual_l3 or 0) + (self.other_actual_l4 or 0)

        self.bifurcation_plan_total = (self.bifurcation_plan_l1 or 0) + (self.bifurcation_plan_l2 or 0) + (self.bifurcation_plan_l3 or 0) + (self.bifurcation_plan_l4 or 0)
        self.bifurcation_actual_total = (self.bifurcation_actual_l1 or 0) + (self.bifurcation_actual_l2 or 0) + (self.bifurcation_actual_l3 or 0) + (self.bifurcation_actual_l4 or 0)

        # Operator totals
        self.total_operators_required_plan = (
            self.ctq_plan_total + self.pdi_plan_total + self.other_plan_total + self.bifurcation_plan_total
        )
        self.total_operators_required_actual = (
            self.ctq_actual_total + self.pdi_actual_total + self.other_actual_total + self.bifurcation_actual_total
        )

        # --- Grand Totals & Gaps ---
        self.grand_total_plan = self.total_operators_required_plan
        self.grand_total_actual = self.total_operators_required_actual

        # Gap for operators
        self.gap_plan = self.total_operators_required_plan - self.total_production_plan
        self.gap_actual = self.total_operators_required_actual - self.total_production_actual

        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.month} {self.year} - {self.factory.factory_name} - {self.line.line_name if self.line else ''}"




import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Assuming your other models (FactoryStructure, LineStructure, etc.) are imported

class DailyProductionData(models.Model):
    # --- The Core Changes ---
    date = models.DateField()
    entry_mode = models.CharField(
        max_length=10,
        choices=[('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly')],
        default='DAILY'
    )
    # This helps group a single weekly or monthly save action together
    batch_id = models.UUIDField(default=uuid.uuid4, editable=False)

    # --- Foreign Keys (Copied from ProductionPlan) ---
    factory = models.ForeignKey(FactoryStructure, on_delete=models.CASCADE)
    shop_floor = models.ForeignKey(ShopFloor, on_delete=models.CASCADE, null=True, blank=True)
    line = models.ForeignKey(LineStructure, on_delete=models.CASCADE, null=True, blank=True)
    station = models.ForeignKey(StationStructure, on_delete=models.CASCADE, null=True, blank=True)

    # --- All Your Essential Data Fields (Copied from ProductionPlan) ---
    # We are keeping EVERY data field you need.

    total_production_plan = models.PositiveIntegerField(default=0)
    total_production_actual = models.PositiveIntegerField(default=0)

    total_operators_required_plan = models.PositiveIntegerField(default=0)
    total_operators_required_actual = models.PositiveIntegerField(default=0)

    attrition_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    absenteeism_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0,
        help_text="Absenteeism rate in percentage (e.g., 5.5 for 5.5%)"
    )

    # CTQ Plan
    ctq_plan_l1 = models.PositiveIntegerField(default=0)
    ctq_plan_l2 = models.PositiveIntegerField(default=0)
    ctq_plan_l3 = models.PositiveIntegerField(default=0)
    ctq_plan_l4 = models.PositiveIntegerField(default=0)
    ctq_plan_total = models.PositiveIntegerField(default=0)
    
    # CTQ Actual
    ctq_actual_l1 = models.PositiveIntegerField(default=0)
    ctq_actual_l2 = models.PositiveIntegerField(default=0)
    ctq_actual_l3 = models.PositiveIntegerField(default=0)
    ctq_actual_l4 = models.PositiveIntegerField(default=0)
    ctq_actual_total = models.PositiveIntegerField(default=0)

    # PDI Plan
    pdi_plan_l1 = models.PositiveIntegerField(default=0)
    pdi_plan_l2 = models.PositiveIntegerField(default=0)
    pdi_plan_l3 = models.PositiveIntegerField(default=0)
    pdi_plan_l4 = models.PositiveIntegerField(default=0)
    pdi_plan_total = models.PositiveIntegerField(default=0)
    
    # PDI Actual
    pdi_actual_l1 = models.PositiveIntegerField(default=0)
    pdi_actual_l2 = models.PositiveIntegerField(default=0)
    pdi_actual_l3 = models.PositiveIntegerField(default=0)
    pdi_actual_l4 = models.PositiveIntegerField(default=0)
    pdi_actual_total = models.PositiveIntegerField(default=0)

    # OTHER Plan
    other_plan_l1 = models.PositiveIntegerField(default=0)
    other_plan_l2 = models.PositiveIntegerField(default=0)
    other_plan_l3 = models.PositiveIntegerField(default=0)
    other_plan_l4 = models.PositiveIntegerField(default=0)
    other_plan_total = models.PositiveIntegerField(default=0)
    
    # OTHER Actual
    other_actual_l1 = models.PositiveIntegerField(default=0)
    other_actual_l2 = models.PositiveIntegerField(default=0)
    other_actual_l3 = models.PositiveIntegerField(default=0)
    other_actual_l4 = models.PositiveIntegerField(default=0)
    other_actual_total = models.PositiveIntegerField(default=0)

    # --- Bifurcation ---
    bifurcation_plan_l1 = models.PositiveIntegerField(default=0)
    bifurcation_plan_l2 = models.PositiveIntegerField(default=0)
    bifurcation_plan_l3 = models.PositiveIntegerField(default=0)
    bifurcation_plan_l4 = models.PositiveIntegerField(default=0)

    bifurcation_actual_l1 = models.PositiveIntegerField(default=0)
    bifurcation_actual_l2 = models.PositiveIntegerField(default=0)
    bifurcation_actual_l3 = models.PositiveIntegerField(default=0)
    bifurcation_actual_l4 = models.PositiveIntegerField(default=0)

    # --- Totals & Gaps ---
    grand_total_plan = models.PositiveIntegerField(default=0)
    grand_total_actual = models.PositiveIntegerField(default=0)
    gap_plan = models.IntegerField(default=0)
    gap_actual = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # This prevents duplicate data for the same line on the same day
        unique_together = ('date', 'line', 'station') # Adjust as needed for your unique context
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.line.line_name if self.line else 'N/A'}"


@receiver(pre_save, sender=DailyProductionData)
def calculate_totals_on_save(sender, instance, **kwargs):
    """
    Automatically calculates all total and gap fields before the instance is saved.
    """
    # 1. Calculate Department Totals
    instance.ctq_plan_total = instance.ctq_plan_l1 + instance.ctq_plan_l2 + instance.ctq_plan_l3 + instance.ctq_plan_l4
    instance.ctq_actual_total = instance.ctq_actual_l1 + instance.ctq_actual_l2 + instance.ctq_actual_l3 + instance.ctq_actual_l4
    instance.pdi_plan_total = instance.pdi_plan_l1 + instance.pdi_plan_l2 + instance.pdi_plan_l3 + instance.pdi_plan_l4
    instance.pdi_actual_total = instance.pdi_actual_l1 + instance.pdi_actual_l2 + instance.pdi_actual_l3 + instance.pdi_actual_l4
    instance.other_plan_total = instance.other_plan_l1 + instance.other_plan_l2 + instance.other_plan_l3 + instance.other_plan_l4
    instance.other_actual_total = instance.other_actual_l1 + instance.other_actual_l2 + instance.other_actual_l3 + instance.other_actual_l4

    # 2. Calculate Bifurcation Totals from department data
    instance.bifurcation_plan_l1 = instance.ctq_plan_l1 + instance.pdi_plan_l1 + instance.other_plan_l1
    instance.bifurcation_actual_l1 = instance.ctq_actual_l1 + instance.pdi_actual_l1 + instance.other_actual_l1
    instance.bifurcation_plan_l2 = instance.ctq_plan_l2 + instance.pdi_plan_l2 + instance.other_plan_l2
    instance.bifurcation_actual_l2 = instance.ctq_actual_l2 + instance.pdi_actual_l2 + instance.other_actual_l2
    instance.bifurcation_plan_l3 = instance.ctq_plan_l3 + instance.pdi_plan_l3 + instance.other_plan_l3
    instance.bifurcation_actual_l3 = instance.ctq_actual_l3 + instance.pdi_actual_l3 + instance.other_actual_l3
    instance.bifurcation_plan_l4 = instance.ctq_plan_l4 + instance.pdi_plan_l4 + instance.other_plan_l4
    instance.bifurcation_actual_l4 = instance.ctq_actual_l4 + instance.pdi_actual_l4 + instance.other_actual_l4

    # 3. Calculate Grand Totals
    instance.grand_total_plan = instance.ctq_plan_total + instance.pdi_plan_total + instance.other_plan_total
    instance.grand_total_actual = instance.ctq_actual_total + instance.pdi_actual_total + instance.other_actual_total
    
    # 4. Calculate Gaps
    instance.gap_plan = instance.total_operators_required_plan - instance.grand_total_plan
    instance.gap_actual = instance.total_operators_required_actual - instance.grand_total_actual




class Notification(models.Model):
    """
    Comprehensive notification model for real-time notifications
    Tracks all system events and user interactions
    """
    NOTIFICATION_TYPES = [
        ('employee_registration', 'Employee Registration'),
        ('level_exam_completed', 'Level Exam Completed'),
        ('training_added', 'Training Added'),
        ('training_updated', 'Training Updated'),
        ('training_scheduled', 'Training Scheduled'),
        ('training_completed', 'Training Completed'),
        ('training_reschedule', 'Training Reschedule'),
        ('refresher_training_scheduled', 'Refresher Training Scheduled'),
        ('refresher_training_completed', 'Refresher Training Completed'),
        ('bending_training_added', 'Bending Training Added'),
        ('level_promotion', 'Level Promotion'),
        ('skill_matrix_updated', 'Skill Matrix Updated'),
        ('machine_allocated', 'Machine Allocated'),
        ('test_assigned', 'Test Assigned'),
        ('evaluation_completed', 'Evaluation Completed'),
        ('milestone_reached', 'Milestone Reached'),
        ('system_alert', 'System Alert'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)

    # Recipients
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    recipient_email = models.EmailField(null=True, blank=True)

    # Related objects
    operator = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey('Level', on_delete=models.CASCADE, null=True, blank=True)
    training_schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, null=True, blank=True)

    # Status tracking
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.recipient or self.recipient_email}"

    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def mark_as_unread(self):
        """Mark notification as unread"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save(update_fields=['is_read', 'read_at'])