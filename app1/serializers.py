

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    employeeid = serializers.CharField(max_length=10)
    role = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=100)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    hq = serializers.CharField(max_length=50)
    factory = serializers.CharField(max_length=50)
    department = serializers.CharField(max_length=50)
    status = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'employeeid', 'first_name', 'last_name',
            'role', 'hq', 'factory', 'department', 'status'
        ]

    def validate_email(self, value):
        """
        Validate email is not already in use.
        Accepts any valid email domain like gmail.com, yahoo.in, etc.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email is already in use.")
        return value

    def validate_password(self, value):
        """
        Validate password strength:
        - Minimum 6 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one number.")
        if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/" for char in value):
            raise ValidationError("Password must contain at least one special character (!@#$%^&*()-_=+[]{}|;:',.<>?/).")
        return value

    def create(self, validated_data):
        """
        Create a new user using create_user method from the User model.
        """
        try:
            return User.objects.create_user(
                email=validated_data['email'],
                employeeid=validated_data['employeeid'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                role=validated_data['role'],
                hq=validated_data['hq'],
                factory=validated_data['factory'],
                department=validated_data['department'],
                password=validated_data['password']
            )
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '').strip()
        password = attrs.get('password', '')

        if not email or not password:
            raise ValidationError({'error': _('Email and password are required.')})

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise ValidationError({'error': _('Invalid email or password.')})

        if not user.is_active:
            raise ValidationError({'error': _('This account is inactive. Please contact support.')})

        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        if not value:
            raise serializers.ValidationError("Refresh token is required for logout.")
        return value













from rest_framework import serializers
from .models import EmployeeMaster, MonthlyAssignment,  OperatorSkill, OperatorTraining, Station, TrainingTopic

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = '__all__'



from rest_framework import serializers
from .models import HQ,Factory,Department,Level,Line

class HQSerializer(serializers.ModelSerializer):
    class Meta:
        model = HQ
        fields = ['id', 'name']


class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = ['id', 'name', 'hq']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'factory']


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = ['id', 'name', 'department']


class LevelSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)

    class Meta:
        model = Level
        fields = ['id', 'name', 'name_display', 'line']




# class OperatorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Operator
#         fields = ['id', 'name', 'code', 'date_of_joining']




from rest_framework import serializers
from .models import MainDepartment, MainLine, SubLine, Station, OperatorSkill
from .models import EmployeeMaster  # Update the path if EmployeeMaster is in another app


class MainDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainDepartment
        fields = ['id', 'name']


class MainLineSerializer(serializers.ModelSerializer):
    department = MainDepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=MainDepartment.objects.all(), source='department', write_only=True)

    class Meta:
        model = MainLine
        fields = ['id', 'name', 'department', 'department_id']


class SubLineSerializer(serializers.ModelSerializer):
    main_line = MainLineSerializer(read_only=True)
    main_line_id = serializers.PrimaryKeyRelatedField(queryset=MainLine.objects.all(), source='main_line', write_only=True)

    class Meta:
        model = SubLine
        fields = ['id', 'name', 'main_line', 'main_line_id']


class StationSerializer(serializers.ModelSerializer):
    sub_line = SubLineSerializer(read_only=True)
    sub_line_id = serializers.PrimaryKeyRelatedField(queryset=SubLine.objects.all(), source='sub_line', write_only=True)

    class Meta:
        model = Station
        fields = [
            'id',
            'sub_line', 'sub_line_id',
            'station_number',
            'skill',
            'minimum_skill_required',
            'min_operator_required'
        ]


class OperatorSkillSerializer(serializers.ModelSerializer):
    operator = serializers.PrimaryKeyRelatedField(queryset=EmployeeMaster.objects.all())
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())

    class Meta:
        model = OperatorSkill
        fields = ['id', 'operator', 'station', 'skill_level', 'sequence']


class TrainingTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingTopic
        fields = ['id', 'name']


class OperatorTrainingSerializer(serializers.ModelSerializer):
    operator = serializers.PrimaryKeyRelatedField(queryset=EmployeeMaster.objects.all())
    topic = serializers.PrimaryKeyRelatedField(queryset=TrainingTopic.objects.all())

    class Meta:
        model = OperatorTraining
        fields = ['id', 'operator', 'topic', 'completed']


class MonthlyAssignmentSerializer(serializers.ModelSerializer):
    operator = serializers.PrimaryKeyRelatedField(queryset=EmployeeMaster.objects.all())
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())

    class Meta:
        model = MonthlyAssignment
        fields = ['id', 'operator', 'station', 'skill_level', 'month']







from rest_framework import serializers
from .models import OperatorLevelTracking

class OperatorLevelTrackingSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.name', read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True)
    milestone_date = serializers.DateField(read_only=True)
    message = serializers.SerializerMethodField()

    class Meta:
        model = OperatorLevelTracking
        fields = ['id', 'operator_name', 'level_name', 'day', 'milestone_date', 'message']

    def get_message(self, obj):
        return f"{obj.operator.name} {obj.level.name} is going to complete today"








from rest_framework import serializers
from .models import OperatorLevelEmailTracking, TrackingEmail

class TrackingEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingEmail
        fields = ['email']

class OperatorLevelEmailTrackingSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.name', read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True)
    milestone_date = serializers.DateField(read_only=True)
    message = serializers.SerializerMethodField()
    emails = TrackingEmailSerializer(many=True, read_only=True)

    class Meta:
        model = OperatorLevelEmailTracking
        fields = ['id', 'operator_name', 'level_name', 'day', 'milestone_date', 'message', 'emails']

    def get_message(self, obj):
        return f"{obj.operator.name} {obj.level.name} is going to complete today"












from rest_framework import serializers
from .models import Machine, MachineAllocation, EmployeeMaster

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'image', 'level', 'process', 'created_at', 'updated_at']


from rest_framework import serializers
from .models import MachineAllocation, Machine, EmployeeMaster, OperatorSkill
from .serializers import MachineSerializer  # Assuming you already have this

class MachineAllocationSerializer(serializers.ModelSerializer):
    machine = MachineSerializer(read_only=True)
    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(),
        source='machine',
        write_only=True
    )
    employee = serializers.StringRelatedField(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeMaster.objects.all(),
        source='employee',
        write_only=True
    )

    class Meta:
        model = MachineAllocation
        fields = [
            'id',
            'machine', 'machine_id',
            'employee', 'employee_id',
            'allocated_at', 'approval_status'
        ]

    def validate(self, data):
        machine = data['machine']
        employee = data['employee']

        required_process = machine.process
        required_level = machine.level
        approval_status = 'pending'  # default

        operator_skills = OperatorSkill.objects.filter(operator=employee, station__skill=required_process)

        for skill in operator_skills:
            try:
                # Extract numeric level from "Level 2" etc.
                level_str = skill.skill_level.strip().lower().replace("level ", "")
                operator_level = int(level_str)
                if operator_level >= required_level:
                    approval_status = 'approved'
                    break
            except:
                continue

        data['approval_status'] = approval_status
        return data

    def create(self, validated_data):
        allocation = MachineAllocation(**validated_data)
        allocation.save()
        return allocation

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance







from rest_framework import serializers
from .models import Days

class DaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ['id', 'level', 'day']



from rest_framework import serializers
from .models import SkillTraining

class SkillTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTraining
        fields = ['id', 'level', 'title']




from rest_framework import serializers
from .models import SubTopic

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = ['id', 'skill_training','day','title']



from rest_framework import serializers
from .models import SubTopic

class SubTopicDaySerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='day.day', read_only=True)  # This accesses the `day` field of the related `Days` model

    class Meta:
        model = SubTopic
        fields = ['id', 'skill_training', 'day', 'day_name', 'title']



from .models import SubTopicContent

class SubTopicContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopicContent
        fields = ['id', 'subtopic', 'title']





from .models import TrainingContent

class TrainingContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingContent
        fields = ['id', 'subtopic_content', 'training_file', 'url_link', 'description']






from rest_framework import serializers
from .models import LevelTwoProduction, LevelTwoLine, LevelTwoSubStation

class LevelTwoSubStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTwoSubStation
        fields = ['id', 'name', 'line']

class LevelTwoLineSerializer(serializers.ModelSerializer):
    substations = LevelTwoSubStationSerializer(many=True, read_only=True)

    class Meta:
        model = LevelTwoLine
        fields = ['id', 'name', 'production', 'substations']

class LevelTwoProductionSerializer(serializers.ModelSerializer):
    leveltwolines = LevelTwoLineSerializer(many=True, read_only=True)

    class Meta:
        model = LevelTwoProduction
        fields = ['id', 'name', 'leveltwolines']








from rest_framework import serializers
from .models import (
    LevelTwoTraineeInfo,
    LevelTwoTrainingTopic,
    LevelTwoOJTDay,
    LevelTwoOJTScore,
    LevelTwoLine,
)

class LevelTwoTraineeInfoSerializer(serializers.ModelSerializer):
    line_name = serializers.CharField(source='line.name', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = LevelTwoTraineeInfo
        fields = ['id','traineeId', 'trainee_name', 'station', 'station_name', 'trainer_name', 'line', 'line_name','training_status']


class LevelTwoTrainingTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTwoTrainingTopic
        fields = '__all__'


class LevelTwoOJTDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTwoOJTDay
        fields = '__all__'


class LevelTwoOJTScoreSerializer(serializers.ModelSerializer):
    trainee = serializers.PrimaryKeyRelatedField(queryset=LevelTwoTraineeInfo.objects.all())
    topic = serializers.PrimaryKeyRelatedField(queryset=LevelTwoTrainingTopic.objects.all())
    day = serializers.PrimaryKeyRelatedField(queryset=LevelTwoOJTDay.objects.all())

    class Meta:
        model = LevelTwoOJTScore
        fields = '__all__'






from rest_framework import serializers
from .models import EmployeeLevelAssignment, LevelTwoTraineeInfo

class EmployeeLevelAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLevelAssignment
        fields = '__all__'

    def create(self, validated_data):
        assignment = super().create(validated_data)

        # Check if the level assigned is "level_2"
        if assignment.level.name == 'level_2':
            LevelTwoTraineeInfo.objects.create(
                traineeId=assignment.operator.pay_code,          # from EmployeeMaster
                trainee_name=assignment.operator.name,           # from EmployeeMaster
                linename=assignment.line.name                    # from LevelTwoLine
            )

        return assignment








class NestedLevelTwoOJTScoreSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(queryset=LevelTwoTrainingTopic.objects.all(), source='topic')
    day_id = serializers.PrimaryKeyRelatedField(queryset=LevelTwoOJTDay.objects.all(), source='day')

    class Meta:
        model = LevelTwoOJTScore
        fields = ['topic_id', 'day_id', 'score']


class NestedLevelTwoTraineeInfoSerializer(serializers.ModelSerializer):
    ojtscores = NestedLevelTwoOJTScoreSerializer(many=True, read_only=True)
    
    station = serializers.PrimaryKeyRelatedField(queryset=LevelTwoSubStation.objects.all())
    line = serializers.PrimaryKeyRelatedField(queryset=LevelTwoLine.objects.all())

    station_name = serializers.CharField(source='station.name', read_only=True)
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = LevelTwoTraineeInfo
        fields = [
            'id',
            'traineeId',
            'trainee_name',
            'station',
            'station_name',
            'trainer_name',
            'line',
            'line_name',
            'training_status', 
            'ojtscores'
        ]

    def create(self, validated_data):
        # If ojtscores is included via custom input (not read_only), handle it
        scores_data = self.initial_data.get('ojtscores')
        trainee = LevelTwoTraineeInfo.objects.create(**validated_data)
        if scores_data:
            for score_data in scores_data:
                LevelTwoOJTScore.objects.create(trainee=trainee, **score_data)
        return trainee

    def update(self, instance, validated_data):
        scores_data = self.initial_data.get('ojtscores')

        # Update trainee fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if scores_data:
            LevelTwoOJTScore.objects.filter(trainee=instance).delete()
            for score_data in scores_data:
                LevelTwoOJTScore.objects.create(trainee=instance, **score_data)

        return instance









#quality level two






from rest_framework import serializers
from .models import (
    LevelTwoQuality,
    LevelTwoQualityLine,
    LevelTwoQualitySubStation,
    LevelTwoQATraineeInfo,
    LevelTwoQATrainingTopic,
    LevelTwoQAOJTDay,
    LevelTwoQAOJTScore,
)

class LevelTwoQualitySubStationSerializer(serializers.ModelSerializer):
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = LevelTwoQualitySubStation
        fields = ['id', 'name', 'line', 'line_name']


class LevelTwoQualityLineSerializer(serializers.ModelSerializer):
    substations = LevelTwoQualitySubStationSerializer(many=True, read_only=True)

    class Meta:
        model = LevelTwoQualityLine
        fields = ['id', 'name', 'quality', 'substations']



class LevelTwoQualitySerializer(serializers.ModelSerializer):
    leveltwolines = LevelTwoQualityLineSerializer(many=True, read_only=True)

    class Meta:
        model = LevelTwoQuality
        fields = ['id', 'name', 'leveltwolines']



class LevelTwoQATraineeInfoSerializer(serializers.ModelSerializer):
    line_name = serializers.CharField(source='line.name', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = LevelTwoQATraineeInfo
        fields = [
            'id',
            'traineeId',
            'trainee_name',
            'station',
            'station_name',
            'trainer_name',
            'line',
            'line_name',
            'training_status'
        ]


class LevelTwoQATrainingTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTwoQATrainingTopic
        fields = '__all__'


class LevelTwoQAOJTDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTwoQAOJTDay
        fields = '__all__'


class LevelTwoQAOJTScoreSerializer(serializers.ModelSerializer):
    trainee = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQATraineeInfo.objects.all())
    topic = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQATrainingTopic.objects.all())
    day = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQAOJTDay.objects.all())

    class Meta:
        model = LevelTwoQAOJTScore
        fields = '__all__'





from rest_framework import serializers
from .models import (
    LevelTwoQATraineeInfo,
    LevelTwoQATrainingTopic,
    LevelTwoQAOJTDay,
    LevelTwoQAOJTScore,
    LevelTwoLine,
)

class LevelTwoQATraineeInfoSerializer(serializers.ModelSerializer):
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = LevelTwoQATraineeInfo
        fields = ['traineeId', 'trainee_name', 'trainer_name', 'line', 'line_name']


class LevelTwoQATrainingTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTwoQATrainingTopic
        fields = '__all__'


class LevelTwoQAOJTDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTwoQAOJTDay
        fields = '__all__'


class LevelTwoQAOJTScoreSerializer(serializers.ModelSerializer):
    trainee = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQATraineeInfo.objects.all())
    topic = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQATrainingTopic.objects.all())
    day = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQAOJTDay.objects.all())

    class Meta:
        model = LevelTwoQAOJTScore
        fields = '__all__'








class NestedLevelTwoQAOJTScoreSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQATrainingTopic.objects.all(), source='topic')
    day_id = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQAOJTDay.objects.all(), source='day')

    class Meta:
        model = LevelTwoQAOJTScore
        fields = ['topic_id', 'day_id', 'score']


class NestedLevelTwoQATraineeInfoSerializer(serializers.ModelSerializer):
    ojtscores = NestedLevelTwoQAOJTScoreSerializer(many=True)

    station = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQualitySubStation.objects.all())
    line = serializers.PrimaryKeyRelatedField(queryset=LevelTwoQualityLine.objects.all())

    station_name = serializers.CharField(source='station.name', read_only=True)
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = LevelTwoQATraineeInfo
        fields = [
            'id',
            'traineeId',
            'trainee_name',
            'station',
            'station_name',
            'trainer_name',
            'line',
            'line_name',
            'training_status',
            'ojtscores'
        ]

    def create(self, validated_data):
        scores_data = validated_data.pop('ojtscores', [])
        trainee = LevelTwoQATraineeInfo.objects.create(**validated_data)

        for score_data in scores_data:
            LevelTwoQAOJTScore.objects.create(trainee=trainee, **score_data)

        return trainee

    def update(self, instance, validated_data):
        scores_data = validated_data.pop('ojtscores', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if scores_data is not None:
            LevelTwoQAOJTScore.objects.filter(trainee=instance).delete()
            for score_data in scores_data:
                LevelTwoQAOJTScore.objects.create(trainee=instance, **score_data)

        return instance












from rest_framework import serializers
from .models import LevelThreeProduction, LevelThreeLine, LevelThreeSubStation


class LevelThreeLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelThreeLine
        fields = ['id', 'name', 'production']


class LevelThreeProductionSerializer(serializers.ModelSerializer):
    level_three_lines = LevelThreeLineSerializer(many=True, read_only=True)

    class Meta:
        model = LevelThreeProduction
        fields = ['id', 'name', 'level_three_lines']


class LevelThreeSubStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelThreeSubStation
        fields = ['id', 'name', 'line']




from rest_framework import serializers
from .models import LevelThreeTraineeInfo, LevelThreeTrainingTopic, LevelThreeOJTDay, LevelThreeOJTScore

class LevelThreeTraineeInfoSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.name', read_only=True)
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = LevelThreeTraineeInfo
        fields = [
            'id',
            'trainee_id',
            'trainee_name',
            'station',
            'station_name',
            'trainer_name',
            'line',
            'line_name',
            'training_status',
        ]

class LevelThreeTrainingTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelThreeTrainingTopic
        fields = '__all__'

class LevelThreeOJTDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelThreeOJTDay
        fields = '__all__'

class LevelThreeOJTScoreSerializer(serializers.ModelSerializer):
    trainee = serializers.PrimaryKeyRelatedField(queryset=LevelThreeTraineeInfo.objects.all())
    topic = serializers.PrimaryKeyRelatedField(queryset=LevelThreeTrainingTopic.objects.all())
    day = serializers.PrimaryKeyRelatedField(queryset=LevelThreeOJTDay.objects.all())

    class Meta:
        model = LevelThreeOJTScore
        fields = '__all__'







from rest_framework import serializers
from .models import (
    LevelThreeTraineeInfo,
    LevelThreeTrainingTopic,
    LevelThreeOJTDay,
    LevelThreeOJTScore,
    LevelThreeSubStation,
    LevelThreeLine,
)



class NestedLevelThreeOJTScoreSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(source='topic', queryset=LevelThreeTrainingTopic.objects.all())
    day_id = serializers.PrimaryKeyRelatedField(source='day', queryset=LevelThreeOJTDay.objects.all())

    class Meta:
        model = LevelThreeOJTScore
        fields = ['topic_id', 'day_id', 'score']





class NestedLevelThreeTraineeInfoSerializer(serializers.ModelSerializer):
    ojtscores = NestedLevelThreeOJTScoreSerializer(many=True, read_only=True)

    station = serializers.PrimaryKeyRelatedField(queryset=LevelThreeSubStation.objects.all())
    line = serializers.PrimaryKeyRelatedField(queryset=LevelThreeLine.objects.all())

    station_name = serializers.CharField(source='station.name', read_only=True)
    line_name = serializers.CharField(source='line.name', read_only=True)
    traineeId = serializers.CharField(source='trainee_id')  # ✅ match model field name

    class Meta:
        model = LevelThreeTraineeInfo
        fields = [
            'id',
            'traineeId',        # ✅ use camelCase here
            'trainee_name',
            'station',
            'station_name',
            'trainer_name',
            'line',
            'line_name',
            'training_status',
            'ojtscores'
        ]


    def create(self, validated_data):
        scores_data = self.initial_data.get('ojtscores')
        trainee = LevelThreeTraineeInfo.objects.create(**validated_data)
        if scores_data:
            for score_data in scores_data:
                LevelThreeOJTScore.objects.create(trainee=trainee, **score_data)
        return trainee

    def update(self, instance, validated_data):
        scores_data = self.initial_data.get('ojtscores')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if scores_data:
            LevelThreeOJTScore.objects.filter(trainee=instance).delete()
            for score_data in scores_data:
                LevelThreeOJTScore.objects.create(trainee=instance, **score_data)

        return instance









from rest_framework import serializers
from .models import LevelThreeQuality, LevelThreeQualityLine,LevelThreeQualitySubStation

class LevelThreeQualitySubStationSerializer(serializers.ModelSerializer):
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = LevelThreeQualitySubStation   # ✅ corrected model
        fields = ['id', 'name', 'line', 'line_name']




class LevelThreeQualityLineSerializer(serializers.ModelSerializer):
    substations = LevelThreeQualitySubStationSerializer(
        many=True, 
        read_only=True, 
        source='levelthree_substations'   # ✅ match the new related_name
    )

    class Meta:
        model = LevelThreeQualityLine
        fields = ['id', 'name', 'quality', 'substations']



class LevelThreeQualitySerializer(serializers.ModelSerializer):
    qualitylevelthreelines = LevelThreeQualityLineSerializer(many=True, read_only=True)

    class Meta:
        model = LevelThreeQuality
        fields = ['id', 'name', 'qualitylevelthreelines']



from rest_framework import serializers
from .models import (
    LevelThreeQATraineeInfo,
    LevelThreeQATrainingTopic,
    LevelThreeQAOJTDay,
    LevelThreeQAOJTScore,
    LevelThreeLine,
)

class LevelThreeQATraineeInfoSerializer(serializers.ModelSerializer):
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = LevelThreeQATraineeInfo
        fields = ['traineeId', 'trainee_name', 'trainer_name', 'line', 'line_name']


class LevelThreeQATrainingTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelThreeQATrainingTopic
        fields = '__all__'


class LevelThreeQAOJTDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelThreeQAOJTDay
        fields = '__all__'


class LevelThreeQAOJTScoreSerializer(serializers.ModelSerializer):
    trainee = serializers.PrimaryKeyRelatedField(queryset=LevelThreeQATraineeInfo.objects.all())
    topic = serializers.PrimaryKeyRelatedField(queryset=LevelThreeQATrainingTopic.objects.all())
    day = serializers.PrimaryKeyRelatedField(queryset=LevelThreeQAOJTDay.objects.all())

    class Meta:
        model = LevelThreeQAOJTScore
        fields = '__all__'







from rest_framework import serializers
from .models import (
    LevelThreeQATraineeInfo,
    LevelThreeQATrainingTopic,
    LevelThreeQAOJTDay,
    LevelThreeQAOJTScore,
    LevelThreeLine,
    LevelThreeQualitySubStation
)

class NestedLevelThreeQAOJTScoreSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(queryset=LevelThreeQATrainingTopic.objects.all(), source='topic')
    day_id = serializers.PrimaryKeyRelatedField(queryset=LevelThreeQAOJTDay.objects.all(), source='day')

    class Meta:
        model = LevelThreeQAOJTScore
        fields = ['topic_id', 'day_id', 'score']


class NestedLevelThreeQATraineeInfoSerializer(serializers.ModelSerializer):
    ojtscores = NestedLevelThreeQAOJTScoreSerializer(many=True)

    station = serializers.PrimaryKeyRelatedField(queryset=LevelThreeQualitySubStation.objects.all())
    line = serializers.PrimaryKeyRelatedField(queryset=LevelThreeQualityLine.objects.all())

    station_name = serializers.CharField(source='station.name', read_only=True)
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = LevelThreeQATraineeInfo
        fields = [
            'id',
            'traineeId',
            'trainee_name',
            'station',
            'station_name',
            'trainer_name',
            'line',
            'line_name',
            'training_status',
            'ojtscores'
        ]

    def create(self, validated_data):
        scores_data = validated_data.pop('ojtscores', [])
        trainee = LevelThreeQATraineeInfo.objects.create(**validated_data)

        for score_data in scores_data:
            LevelThreeQAOJTScore.objects.create(trainee=trainee, **score_data)

        return trainee

    def update(self, instance, validated_data):
        scores_data = validated_data.pop('ojtscores', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if scores_data is not None:
            LevelThreeQAOJTScore.objects.filter(trainee=instance).delete()
            for score_data in scores_data:
                LevelThreeQAOJTScore.objects.create(trainee=instance, **score_data)

        return instance



from rest_framework import serializers
from .models import ARVRTrainingContent

class ARVRTrainingContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARVRTrainingContent
        # fields = ['id', 'description', 'arvr_file']
        fields = '_all_'


from rest_framework import serializers
from .models import ARVRTrainingContent

class ARVRTrainingContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARVRTrainingContent
        # fields = ['id', 'description', 'arvr_file']
        fields = '__all__'







from rest_framework import serializers
from .models import MCQQuestion

class MCQQuestionSerializer(serializers.ModelSerializer):
    # Optional: Display subtopic content title instead of just ID
    subtopic_content_title = serializers.CharField(source='subtopic_content.title', read_only=True)

    class Meta:
        model = MCQQuestion
        fields = [
            'id',
            'subtopic_content',         # ForeignKey field (write access)
            'subtopic_content_title',   # Read-only title (optional)
            'question',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_answer'
        ]

    def validate(self, data):
        options = [
            data.get('option_a'),
            data.get('option_b'),
            data.get('option_c'),
            data.get('option_d')
        ]
        if data.get('correct_answer') not in options:
            raise serializers.ValidationError("Correct answer must match one of the options.")
        return data




from rest_framework import serializers
from .models import BiometricAttendance

class BiometricAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiometricAttendance
        fields = '__all__'





from rest_framework import serializers
from .models import MultiSkilling

from rest_framework import serializers
from .models import MultiSkilling

# class NewMultiSkillingSerializer(serializers.ModelSerializer):
#     card_no = serializers.CharField(source='employee.card_no', read_only=True)

#     class Meta:
#         model = MultiSkilling
#         fields = [
#             'id',
#             'employee',
#             'card_no',
#             'station',
#             'skill_level',
#             'start_date',
#             'end_date',
#             'notes',
#             'status'
# ]

class RefreshMultiSkillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiSkilling
        fields = [
            'id',
            'employee',
            'skill',
            'notes',
            'status',
            'reason',
            'refreshment_date',
        ]




from rest_framework import serializers
from .models import TrainingReport

class TrainingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingReport
        fields = '__all__'




from rest_framework import serializers
from .models import UnifiedDefectReport

class UnifiedDefectReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnifiedDefectReport
        fields = '__all__'

from rest_framework import serializers

class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()








# serializers.py
from rest_framework import serializers
from .models import EmployeeMaster

class EmployeeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['id', 'name']  # Include 'id' optionally


# serializers.py
from rest_framework import serializers
from .models import EmployeeMaster

class EmployeeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['id', 'name']  # Include 'id' optionally


# easy test


from rest_framework import serializers
from .models import  *


class KeyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyEvent
        fields = '__all__'

class ConnectEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectEvent
        fields = '__all__'




class VoteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteEvent
        fields = '__all__'

# dynamic questions



class QuestionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPaper
        fields = ['id', 'name']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_index', 'question_paper']




class TestSessionSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    level_name = serializers.CharField(source='level', read_only=True)  # ✅ directly from string
    skill_name = serializers.CharField(source='skill.skill', default='', read_only=True)

    class Meta:
        model = TestSession
        fields = ['id', 'key_id', 'employee', 'employee_name', 'level', 'level_name', 'skill', 'skill_name']






class ScoreSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(source='employee.id')
    name = serializers.CharField(source='employee.name')
    section = serializers.CharField(source='employee.section', default='')
    total_questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Score
        fields = [
            'employee_id', 'name', 'section',
            'marks', 'percentage', 'total_questions', 'passed', 'test_name', 'created_at'
        ]

    def get_percentage(self, obj):
        total = self.get_total_questions(obj)
        return (obj.marks / total) * 100 if total > 0 else 0

    def get_total_questions(self, obj):
        if obj.test:
            return obj.test.questions.count()
        return 0





class SimpleScoreSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    name = serializers.CharField()
    marks = serializers.IntegerField()
    percentage = serializers.FloatField()
    level_name = serializers.CharField()
    skill_name = serializers.CharField()
    section = serializers.CharField()


    





#Employee Card 


class OperatorCardSkillSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.name', read_only=True)
    station_skill = serializers.CharField(source='station.skill', read_only=True)

    class Meta:
        model = OperatorSkill
        fields = ['id', 'operator_name', 'station_skill', 'skill_level', 'sequence']






from rest_framework import serializers
from .models import Score

class CardScoreSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = Score
        fields = [
            'id',
            'employee_name',
            'test_name',     # just use directly if it's a model field
            'marks',
            'percentage',    # must exist in model
            'passed',        # must exist in model
            'created_at'
        ]







from rest_framework import serializers
from .models import MultiSkilling

class CardMultiSkillingSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    station_number = serializers.IntegerField(source='station.station_number', read_only=True)
    skill_level_value = serializers.CharField(source='skill_level.skill_level', read_only=True)
    skill = serializers.CharField(source='station.skill', read_only=True, allow_null=True)

    class Meta:
        model = MultiSkilling
        fields = [
            'id',
            'employee_name',
            'station_number',
            'skill',
            'skill_level_value',
            'start_date',
            'end_date',
            'notes',
            'status',
            'reason',
            'refreshment_date'
        ]







from rest_framework import serializers
from .models import RefreshmentTraining

class CardRefreshmentTrainingSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    card_no = serializers.CharField(source='employee.card_no', read_only=True)
    station_number = serializers.IntegerField(source='station.station_number', read_only=True)
    skill_name = serializers.CharField(source='skill.skill', read_only=True)
    skill_level_value = serializers.CharField(source='skill_level.skill_level', read_only=True)

    class Meta:
        model = RefreshmentTraining
        fields = [
            'id',
            'employee_name',
            'card_no',
            'station_number',
            'skill_name',
            'skill_level_value',
            'start_date',
            'end_date',
            'reason_for_refreshment',
        ]


# your_app/serializers.py

from rest_framework import serializers
from .models import Schedule # Make sure Schedule is imported
# your_app/serializers.py

from rest_framework import serializers
from .models import Schedule

# ... other serializers ...

# THIS IS THE CORRECTED VERSION
# your_app/serializers.py

from rest_framework import serializers
from .models import Schedule

# ... other serializers ...

# THIS IS THE UPDATED VERSION
class CardScheduleSerializer(serializers.ModelSerializer):
    """
    This serializer takes a Schedule object and formats it for the
    employee history card.
    """
    
    # ★ GET related names instead of IDs
    trainer_name = serializers.CharField(source='trainer.name', read_only=True, allow_null=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True, allow_null=True)

    # ★ RENAME 'training_name.topic' to be more descriptive
    topic = serializers.CharField(source='training_name.topic', read_only=True)
    
    # ★ GET the category name
    category_name = serializers.CharField(source='training_category.name', read_only=True)

    class Meta:
        model = Schedule
        # ★ UPDATE the fields list with the new data
        fields = [
            'id',
            'topic',
            'category_name',
            'trainer_name',
            'venue_name',
            'status',
            # 'created_at',
            'date'
            # 'time',  # Let's add time as well, it's useful!
        ]
    # --- ★ START: ADD THESE MISSING METHODS ★ ---

    


from rest_framework import serializers
from .models import EmployeeMaster

class CardEmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = [
            'id', 'pay_code', 'card_no', 'name', 'guardian_name', 'sex', 'birth_date',
            'department', 'section', 'desig_category', 'joining_date',
            'auth_shift', 'shift_type', 'shift_pattern',
            'first_weekly_off', 'second_weekly_off', 'second_weekly_off_fh',
            'ot_allowed_rate', 'round_the_clock'
        ]






class StationByLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'




class SubLineByMainLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLine
        fields = '__all__'





class MainLineByDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainLine
        fields = '__all__'







from .models import ManagementReview

class TrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementReview
        fields = ['month_year', 'new_operators_joined', 'new_operators_trained', 
                 'total_training_plans', 'total_trainings_actual']

class DefectsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementReview
        fields = ['month_year', 'total_defects_msil', 'ctq_defects_msil', 
                 'total_defects_tier1', 'ctq_defects_tier1', 
                 'total_internal_rejection', 'ctq_internal_rejection']

class OperatorsChartSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    operators_joined = serializers.IntegerField(source='new_operators_joined')
    operators_trained = serializers.IntegerField(source='new_operators_trained')
    
    class Meta:
        model = ManagementReview
        fields = ['year', 'month_year', 'operators_joined', 'operators_trained']
    
    def get_year(self, obj):
        return obj.month_year.year

class TrainingPlansChartSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    training_plans = serializers.IntegerField(source='total_training_plans')
    trainings_actual = serializers.IntegerField(source='total_trainings_actual')
    
    class Meta:
        model = ManagementReview
        fields = ['year', 'month_year', 'training_plans', 'trainings_actual']
    
    def get_year(self, obj):
        return obj.month_year.year
    


    
from rest_framework import serializers
from .models import ManagementReview

class DefectsChartSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    defects_msil = serializers.IntegerField(source='total_defects_msil')  # renaming, valid
    ctq_defects_msil = serializers.IntegerField()  # FIXED: no need for source

    class Meta:
        model = ManagementReview
        fields = ['year', 'month_year', 'defects_msil', 'ctq_defects_msil']

    def get_year(self, obj):
        return obj.month_year.year



from rest_framework import serializers

class ManagementReviewUploadSerializer(serializers.Serializer):
    file = serializers.FileField()





# serializers.py

from rest_framework import serializers
from .models import ManagementReview

class ManagementReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementReview
        fields = '__all__'


from rest_framework import serializers
from .models import CompanyLogo

class CompanyLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyLogo
        fields = ['id', 'name', 'logo', 'uploaded_at']








from rest_framework import viewsets
from .models import CompanyLogo
from .serializers import CompanyLogoSerializer

class CompanyLogoViewSet(viewsets.ModelViewSet):
    queryset = CompanyLogo.objects.all()
    serializer_class = CompanyLogoSerializer



from rest_framework import serializers
from .models import MachineAllocation

class MachineAllocationApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineAllocation
        fields = ['id', 'approval_status']

# serializers.py

from rest_framework import serializers
from .models import EmployeeMaster, MachineAllocation

class EmployeeWithStatusSerializer(serializers.ModelSerializer):
    approval_status = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeMaster
        fields = ['id', 'name', 'approval_status']  # include fields as needed

    def get_approval_status(self, obj):
        machine_id = self.context.get('machine_id')
        if machine_id:
            allocation = MachineAllocation.objects.filter(machine_id=machine_id, employee=obj).first()
            if allocation:
                return allocation.approval_status
        return None
    
from rest_framework import serializers
from .models import Department

class FactoryWiseDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']



from rest_framework import serializers
from .models import AdvancedManpowerCTQ, Factory, Department

class NewAdvancedManpowerCTQSerializer(serializers.ModelSerializer):
    factory_name = serializers.CharField(source='factory.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = AdvancedManpowerCTQ
        fields = [
            'id',
            'month_year_ctq',
            'total_stations_ctq',
            'operator_required_ctq',
            'operator_availability_ctq',
            'buffer_manpower_required_ctq',
            'buffer_manpower_availability_ctq',
            'attrition_trend_ctq',
            'absentee_trend_ctq',
            'planned_units_ctq',
            'actual_production_ctq',
            'factory',             # writeable field (ID)
            'department',          # writeable field (ID)
            'factory_name',        # read-only field for display
            'department_name'      # read-only field for display
        ]


# serializers.py


from rest_framework import serializers
from .models import AdvancedManpowerCTQ

class OperatorTrendSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdvancedManpowerCTQ
        fields = ['month', 'operator_required_ctq', 'operator_availability_ctq']

    def get_month(self, obj):
        return obj.month_year_ctq.strftime('%B %Y')  # Example: "July 2025"







# serializers.py

class BufferManpowerTrendSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdvancedManpowerCTQ
        fields = ['month', 'buffer_manpower_required_ctq', 'buffer_manpower_availability_ctq']

    def get_month(self, obj):
        return obj.month_year_ctq.strftime('%B %Y')  # e.g., "July 2025"





# serializers.py

class AttritionTrendSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdvancedManpowerCTQ
        fields = ['month', 'attrition_trend_ctq']

    def get_month(self, obj):
        return obj.month_year_ctq.strftime('%B %Y')  # Example: "July 2025"





# serializers.py

class AbsenteeTrendSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdvancedManpowerCTQ
        fields = ['month', 'absentee_trend_ctq']

    def get_month(self, obj):
        return obj.month_year_ctq.strftime('%B %Y')  # e.g., "July 2025"




# serializers.py

from rest_framework import serializers
from .models import AdvancedManpowerCTQ

class AdvancedManpowerCTQSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedManpowerCTQ
        fields = [
            'month_year_ctq',
            'total_stations_ctq',
            'operator_required_ctq',
            'operator_availability_ctq',
            'buffer_manpower_required_ctq',
            'buffer_manpower_availability_ctq',
        ]




# serializers.py

from rest_framework import serializers
from .models import AdvancedManpowerCTQ

class OperatorTrendSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdvancedManpowerCTQ
        fields = ['month', 'operator_required_ctq', 'operator_availability_ctq']

    def get_month(self, obj):
        return obj.month_year_ctq.strftime('%B %Y')  # Example: "July 2025"







# serializers.py

class BufferManpowerTrendSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdvancedManpowerCTQ
        fields = ['month', 'buffer_manpower_required_ctq', 'buffer_manpower_availability_ctq']

    def get_month(self, obj):
        return obj.month_year_ctq.strftime('%B %Y')  # e.g., "July 2025"





# serializers.py

class AttritionTrendSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdvancedManpowerCTQ
        fields = ['month', 'attrition_trend_ctq']

    def get_month(self, obj):
        return obj.month_year_ctq.strftime('%B %Y')  # Example: "July 2025"





# serializers.py

class AbsenteeTrendSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdvancedManpowerCTQ
        fields = ['month', 'absentee_trend_ctq']

    def get_month(self, obj):
        return obj.month_year_ctq.strftime('%B %Y')  # e.g., "July 2025"
    

from rest_framework import serializers
from .models import OperatorRequirement, Factory, Department

class OperatorRequirementSerializer(serializers.ModelSerializer):
    factory_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = OperatorRequirement
        fields = [
            'id',
            'factory',
            'department',
            'month',
            'level',
            'operator_required',
            'operator_available',
            'factory_name',
            'department_name',
        ]

    def get_factory_name(self, obj):
        return obj.factory.name if obj.factory else None

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

    def validate(self, data):
        factory = data.get('factory')
        department = data.get('department')

        # Optional: Validate department belongs to the selected factory
        if department and factory and department.factory_id != factory.id:
            raise serializers.ValidationError("The selected department does not belong to the given factory.")
        return data
    



from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'title', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']







from rest_framework import serializers
from .models import Score, EmployeeMaster

class LevelOneEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = '__all__'

class LevelOneScoreSerializer(serializers.ModelSerializer):
    employee = LevelOneEmployeeSerializer()

    class Meta:
        model = Score
        fields = ['employee', 'marks', 'test_name', 'percentage', 'passed', 'level', 'created_at']






from rest_framework import serializers
from .models import Score, Station, LevelTwoTraineeInfo

class LevelTwoStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'skill']

class LevelTwoScoreMiniSerializer(serializers.ModelSerializer):
    skill = StationSerializer()

    class Meta:
        model = Score
        fields = ['passed', 'skill']

class LevelTwoTraineeInfoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTwoTraineeInfo
        fields = ['traineeId', 'station', 'line', 'training_status']

class LevelTwoGroupedEmployeeScoreSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    trainee_info = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()

    def get_trainee_info(self, obj):
        from .models import LevelTwoTraineeInfo
        try:
            trainee = LevelTwoTraineeInfo.objects.get(trainee_name=obj['employee_name'])
            return LevelTwoTraineeInfoMiniSerializer(trainee).data
        except LevelTwoTraineeInfo.DoesNotExist:
            return None

    def get_scores(self, obj):
        scores = obj['scores']
        return LevelTwoScoreMiniSerializer(scores, many=True).data








from rest_framework import serializers
from .models import Score, Station, LevelThreeTraineeInfo  # <-- Make sure this model exists

class LevelThreeStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'skill']

class LevelThreeScoreMiniSerializer(serializers.ModelSerializer):
    skill = LevelThreeStationSerializer()

    class Meta:
        model = Score
        fields = ['passed', 'skill']

class LevelThreeTraineeInfoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelThreeTraineeInfo
        fields = ['traineeId', 'station', 'line', 'training_status']

class LevelThreeGroupedEmployeeScoreSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    trainee_info = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()

    def get_trainee_info(self, obj):
        try:
            trainee = LevelThreeTraineeInfo.objects.get(trainee_name=obj['employee_name'])
            return LevelThreeTraineeInfoMiniSerializer(trainee).data
        except LevelThreeTraineeInfo.DoesNotExist:
            return None

    def get_scores(self, obj):
        scores = obj['scores']
        return LevelThreeScoreMiniSerializer(scores, many=True).data



# level0

from rest_framework import serializers
from .models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    
    phoneNumber = serializers.CharField(source='phone_number')
    tempId = serializers.CharField(source='temp_id',read_only=True) # read_only=True FOR TEMP ID
    

    class Meta:
        model = UserInfo
        fields = [
            'id', 'firstName',  'tempId', 'email', 'phoneNumber', 'sex',
            'created_at', 'updated_at', 'is_active', 
        ]
        extra_kwargs = {
            'email': {'required': False, 'allow_null': True},
            'phoneNumber': {'required': True},
            'sex': {'required': True},
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'is_active': {'read_only': True},
        }

    # def create(self, validated_data):
    #     return UserInfo.objects.create(**validated_data)  

    def create(self, validated_data):
        # Convert empty string email to None
        if 'email' in validated_data and validated_data['email'] == '':
            validated_data['email'] = None
        return UserInfo.objects.create(**validated_data)
  

class UserInfoUpdateSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    phoneNumber = serializers.CharField(source='phone_number')
    tempId = serializers.CharField(source='temp_id')  # writable by default
    

    class Meta:
        model = UserInfo
        fields = [
            'id', 'firstName', 'tempId', 'email', 'phoneNumber', 'sex',
            'created_at', 'updated_at', 'is_active'
        ]
        extra_kwargs = {
            'email': {'required': False, 'allow_null': True},
            'phoneNumber': {'required': True},
            'sex': {'required': True},
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'is_active': {'read_only': True},
        }



from rest_framework import serializers
from .models import HumanBodyCheck

class HumanBodyCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanBodyCheck
        fields = '__all__'
        read_only_fields = ['check_date', 'overall_status']
        
    def validate(self, data):
        # Ensure temp_id is provided
        if not data.get('temp_id'):
            raise serializers.ValidationError("temp_id is required")
            
        # Validate status fields
        status_fields = [
            'color_vision', 'eye_movement', 'fingers_functionality',
            'hand_deformity', 'joint_mobility', 'hearing', 'bending_ability'
        ]
        
        for field in status_fields:
            if field in data and data[field] not in ['pass', 'fail', 'pending']:
                raise serializers.ValidationError(f"{field} must be 'pass', 'fail', or 'pending'")
                
        return data
    

class TrainingBatchSerializer(serializers.ModelSerializer):
    """ Serializer for the TrainingBatch model. """
    class Meta:
        model = TrainingBatch
        fields = ['batch_id', 'is_active', 'created_at']


class TrainingAttendanceSerializer(serializers.ModelSerializer):
    """ Serializer for creating/updating individual attendance records. """
    user = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all())
    # The attendance_date is set by the server, so it's read-only for clients.
    attendance_date = serializers.DateField(read_only=True) 

    class Meta:
        model = TrainingAttendance
        fields = ['user', 'batch', 'day_number', 'status', 'attendance_date']


# ... your other serializers ...

class CardTrainingAttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for showing attendance in the Employee Card view.
    """
    # Get the batch_id string directly instead of the related object ID
    batch = serializers.CharField(source='batch.batch_id', read_only=True)

    class Meta:
        model = TrainingAttendance
        # These fields match what your React interface expects
        fields = ['id', 'batch', 'day_number', 'status', 'attendance_date']


class UserForAttendanceSerializer(serializers.ModelSerializer):
    """ A simplified User serializer for nesting inside the attendance detail view. """
    attendances = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = ['id', 'first_name', 'temp_id', 'attendances']

    def get_attendances(self, obj):
        batch_id = self.context.get('batch_id')
        if not batch_id:
            return {}
        attendances = TrainingAttendance.objects.filter(user=obj, batch=batch_id)
        return {att.day_number: att.status for att in attendances}
    



class BatchAttendanceDetailSerializer(serializers.Serializer):
    """
    Custom serializer for the main attendance page response.
    Combines batch info, the next day to mark, and the list of users.
    """
    batch_id = serializers.CharField()
    next_training_day_to_mark = serializers.IntegerField(allow_null=True)
    is_completed = serializers.BooleanField()
    users = UserForAttendanceSerializer(many=True)



    

from rest_framework import serializers
from .models import SDCOrientationFeedback

class SDCOrientationFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = SDCOrientationFeedback
        fields = [
            'id',
            'user',
            'pay_code',
            'card_no',
            'sex',
            'birth_date',
            'guardian_name',
            'department',
            'section',
            'desig_category',
            'joining_date',
          
        ]






class ListUserInfoWithBodyCheckSerializer(serializers.ModelSerializer):
    body_checks = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = [
            'first_name', 'temp_id', 'email', 'phone_number', 
            'sex', 'created_at', 'is_active', 'body_checks'
        ]

    def get_body_checks(self, obj):
        checks = HumanBodyCheck.objects.filter(temp_id=obj.temp_id)
        return HumanBodyCheckSerializer(checks, many=True).data

from rest_framework import serializers
from .models import UserInfo, HumanBodyCheck, SDCOrientationFeedback

class FetchHumanBodyCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanBodyCheck
        fields = '__all__'

class FetchSDCOrientationFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDCOrientationFeedback
        fields = '__all__'

class FetchUserInfoSerializer(serializers.ModelSerializer):
    body_check = serializers.SerializerMethodField()
    orientation_feedbacks = FetchSDCOrientationFeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = UserInfo
        fields = [
           'id', 'first_name', 'temp_id', 'email', 'phone_number',
            'sex', 'created_at', 'updated_at', 'is_active',
            'body_check', 'orientation_feedbacks'
        ]

    def get_body_check(self, obj):
        body_check = HumanBodyCheck.objects.filter(temp_id=obj.temp_id, overall_status='pass').first()
        return FetchHumanBodyCheckSerializer(body_check).data if body_check else None

# Refreshment Training

#serializers.py 

from rest_framework import serializers
from .models import Training_category, Curriculum, CurriculumContent, Trainer_name, Venues, Schedule, EmployeeMaster,EmployeeAttendance,RescheduleLog

class Training_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_category
        fields = '__all__'

class CurriculumSerializer(serializers.ModelSerializer):
    category = Training_categorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Training_category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Curriculum
        fields = ['id', 'category', 'category_id', 'topic', 'description']

class CurriculumContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumContent
        fields = '__all__'

class Trainer_nameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer_name
        fields = '__all__'

class VenuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venues
        fields = '__all__'

class RefresherOperatorMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['id', 'pay_code', 'name']

class ScheduleSerializer(serializers.ModelSerializer):
    training_category = Training_categorySerializer(read_only=True)
    training_category_id = serializers.PrimaryKeyRelatedField(queryset=Training_category.objects.all(), source='training_category', write_only=True)

    training_name = CurriculumSerializer(read_only=True)
    training_name_id = serializers.PrimaryKeyRelatedField(queryset=Curriculum.objects.all(), source='training_name', write_only=True)

    trainer = Trainer_nameSerializer(read_only=True)
    trainer_id = serializers.PrimaryKeyRelatedField(queryset=Trainer_name.objects.all(), source='trainer', write_only=True)

    venue = VenuesSerializer(read_only=True)
    venue_id = serializers.PrimaryKeyRelatedField(queryset=Venues.objects.all(), source='venue', write_only=True)

    employees = RefresherOperatorMasterSerializer(many=True, read_only=True)
    employee_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=EmployeeMaster.objects.all(), write_only=True, source='employees')

    class Meta:
        model = Schedule
        fields = ['id', 'training_category', 'training_category_id', 'training_name', 'training_name_id',
                  'trainer', 'trainer_id', 'venue', 'venue_id', 'status', 'date', 'time',
                  'employees','employee_ids']


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = [
            'id',
            'schedule',
            'employee',
            'status',
            'notes',
            'reschedule_date',
            'reschedule_time',
            'reschedule_reason',
            'updated_at',
        ]
        read_only_fields = ['updated_at']


class RescheduleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RescheduleLog
        fields='__all__'



from rest_framework import serializers
from rest_framework import serializers
from .models import NewMultiSkilling
 # assume you have these


class NewMultiSkillingSerializer(serializers.ModelSerializer):
    # Nested for GET
    employee = EmployeeSerializer(read_only=True)
    operation = StationSerializer(read_only=True)
    skill_level = LevelSerializer(read_only=True)

    # IDs for POST/PUT
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeMaster.objects.all(), source="employee", write_only=True
    )
    operation_id = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(), source="operation", write_only=True, required=False, allow_null=True
    )
    skill_level_id = serializers.PrimaryKeyRelatedField(
        queryset=Level.objects.all(), source="skill_level", write_only=True
    )

    class Meta:
        model = NewMultiSkilling
        fields = [
            "id",
            "employee", "employee_id",
            "operation", "operation_id",
            "skill_level", "skill_level_id",
             "start_date", "end_date", 
            "remarks",
            "status",
        ]
        read_only_fields = ["status"]  # since it's auto-set in model.save()



# Hanchou & Shokuchou 

from rest_framework import serializers
from .models import HanchouExamQuestion

class HanchouExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HanchouExamQuestion
        fields = '__all__'

from rest_framework import serializers
from django.utils import timezone
from .models import HanchouExamResult, EmployeeMaster
# IMPORTANT: adjust this import to where your EmployeeSerializer actually lives
from .serializers import EmployeeSerializer  # or from .employee_serializers import EmployeeSerializer

class HanchouExamResultSerializer(serializers.ModelSerializer):
    """
    Handles serialization for Hanchou Exam Results.
    - Expects `employee_id`, `started_at`, `submitted_at`, `total_questions`, and `score` from the client.
    - Calculates `duration_seconds` automatically.
    - The model's `save` method handles calculating `passed`.
    - Returns the full result object, including nested employee details, on read.
    """

    # --- Fields for Reading Data (Output) ---
    # Use your EmployeeSerializer to show nested employee details when retrieving results.
    employee = EmployeeSerializer(read_only=True)
    # A custom read-only field to show the calculated percentage.
    percentage = serializers.FloatField(read_only=True)


    # --- Field for Writing Data (Input) ---
    # This field accepts the primary key (the ID) of an employee from the frontend.
    # `source='employee'` tells DRF to use this ID to populate the 'employee' model field.
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeMaster.objects.all(),
        source='employee',
        write_only=True
    )

    class Meta:
        model = HanchouExamResult
        # List ALL fields that should be part of the API representation.
        # We removed 'attempt_id' and 'exam_date' as they are not in your model.
        fields = [
            'id',
            'employee',           # For reading (nested object)
            'employee_id',        # For writing (just the ID)
            'exam_name',
            'started_at',
            'submitted_at',
            'total_questions',
            'score',
            'duration_seconds',
            'pass_mark_percent',
            'passed',
            'percentage',
            'remarks'
        ]
        # Fields that are calculated or set by the server and should not be accepted from the client.
        read_only_fields = (
            'id', 
            'exam_name', 
            'duration_seconds', 
            'passed', 
            'percentage'
        )

    def validate(self, attrs):
        """
        Perform cross-field validation.
        """
        # Ensure submitted_at is not earlier than started_at.
        if attrs.get('started_at') and attrs.get('submitted_at'):
            if attrs['submitted_at'] < attrs['started_at']:
                raise serializers.ValidationError({"submitted_at": "Submission time cannot be earlier than start time."})

        # Ensure score is not greater than total_questions.
        if attrs.get('score') is not None and attrs.get('total_questions') is not None:
            if attrs['score'] > attrs['total_questions']:
                raise serializers.ValidationError({"score": "Score cannot be greater than total questions."})

        return attrs

    def create(self, validated_data):
        """
        Override the create method to add custom logic.
        """
        started_at = validated_data.get('started_at')
        submitted_at = validated_data.get('submitted_at')

        # Automatically calculate the duration if timestamps are provided.
        if started_at and submitted_at:
            duration = submitted_at - started_at
            validated_data['duration_seconds'] = int(duration.total_seconds())

        # Create the HanchouExamResult instance using the validated data.
        # The model's save() method will handle setting the `passed` field.
        return HanchouExamResult.objects.create(**validated_data)


from rest_framework import serializers
from .models import ShokuchouExamQuestion, ShokuchouExamResult, EmployeeMaster
# IMPORTANT: adjust import path to wherever EmployeeSerializer is defined
from .serializers import EmployeeSerializer  


# --- SHO QUESTION SERIALIZER ---
class ShokuchouExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShokuchouExamQuestion
        fields = '__all__'


# --- SHO RESULT SERIALIZER ---
class ShokuchouExamResultSerializer(serializers.ModelSerializer):
    """
    Handles serialization for Shokuchou Exam Results.
    - Expects `employee_id`, `sho_started_at`, `sho_submitted_at`, `sho_total_questions`, and `sho_score` from the client.
    - Calculates `sho_duration_seconds` automatically.
    - The model's `save` method handles calculating `sho_passed`.
    - Returns the full result object, including nested employee details, on read.
    """

    # --- Output fields ---
    employee = EmployeeSerializer(read_only=True)
    sho_percentage = serializers.FloatField(read_only=True)

    # --- Input field ---
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeMaster.objects.all(),
        source='employee',
        write_only=True
    )

    class Meta:
        model = ShokuchouExamResult
        fields = [
            'id',
            'employee',             # read
            'employee_id',          # write
            'sho_exam_name',
            'sho_started_at',
            'sho_submitted_at',
            'sho_total_questions',
            'sho_score',
            'sho_duration_seconds',
            'sho_pass_mark_percent',
            'sho_passed',
            'sho_percentage',
            'sho_remarks'
        ]
        read_only_fields = (
            'id',
            'sho_exam_name',
            'sho_duration_seconds',
            'sho_passed',
            'sho_percentage'
        )

    def validate(self, attrs):
        """
        Cross-field validation for Shokuchou Exam.
        """
        if attrs.get('sho_started_at') and attrs.get('sho_submitted_at'):
            if attrs['sho_submitted_at'] < attrs['sho_started_at']:
                raise serializers.ValidationError(
                    {"sho_submitted_at": "Submission time cannot be earlier than start time."}
                )

        if attrs.get('sho_score') is not None and attrs.get('sho_total_questions') is not None:
            if attrs['sho_score'] > attrs['sho_total_questions']:
                raise serializers.ValidationError(
                    {"sho_score": "Score cannot be greater than total questions."}
                )

        return attrs

    def create(self, validated_data):
        """
        Automatically calculate sho_duration_seconds before saving.
        """
        started_at = validated_data.get('sho_started_at')
        submitted_at = validated_data.get('sho_submitted_at')

        if started_at and submitted_at:
            duration = submitted_at - started_at
            validated_data['sho_duration_seconds'] = int(duration.total_seconds())

        return ShokuchouExamResult.objects.create(**validated_data)


# your_app/serializers.py
class CardShokuchouExamResultSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for Shokuchou results, formatted for the Employee Card view.
    """
    exam_name = serializers.CharField(source='sho_exam_name')
    score = serializers.IntegerField(source='sho_score')
    total_questions = serializers.IntegerField(source='sho_total_questions')
    percentage = serializers.FloatField(source='sho_percentage')
    passed = serializers.BooleanField(source='sho_passed')
    submitted_at = serializers.DateTimeField(source='sho_submitted_at')

    class Meta:
        model = ShokuchouExamResult
        fields = (
            'id',
            'exam_name',
            'score',
            'total_questions',
            'percentage',
            'passed',
            'submitted_at',
        )



# yourapp/serializers.py

# ... other imports ...
from .models import HanchouExamResult # Make sure to import the model

# ... other serializers ...

# ★★★ NEW SERIALIZER FOR THE EMPLOYEE HISTORY CARD ★★★
class CardHanchouExamResultSerializer(serializers.ModelSerializer):
    """
    A read-only serializer to format Hanchou exam results for the employee card view.
    It provides a clean, flat structure.
    """
    # The 'percentage' field is a @property on the model, so we declare it here
    # to ensure it's included in the serialization.
    percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = HanchouExamResult
        # List the specific fields you want to show in "Card 6" of your React component.
        fields = [
            'id',
            'exam_name',
            'score',
            'total_questions',
            'percentage',
            'passed',
            'submitted_at',
        ]


from .models import HanContent,ShoContent,ShoTrainingContent,ShoSubtopic
from .models import HanTrainingContent

# your_app/serializers.py

from rest_framework import serializers
from .models import HanContent, HanSubtopic, HanTrainingContent

from django.urls import reverse # <-- IMPORT reverse


# --- THIS IS THE CORRECTED HAN SERIALIZER ---
class HanTrainingContentSerializer(serializers.ModelSerializer):
    # This field accepts the file during an upload (POST/PUT).
    # It won't be included in the response (GET).
    training_file = serializers.FileField(write_only=True, required=False)

    # This field is what your React frontend will receive.
    # It's read-only because it's generated by the method below.
    training_file_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HanTrainingContent
        # FIX #1: Added 'training_file_url' to this list.
        fields = [
            'id',
            'description',
            'training_file',       # For uploads
            'training_file_url',   # For downloads
            'url_link',
            'han_subtopic'
        ]
        # This part is correct, it hides the subtopic object from the response.
        extra_kwargs = {'han_subtopic': {'write_only': True}}

    # FIX #2: Renamed this method from get_training_file to get_training_file_url
    # The name MUST match the field it's for: get_<field_name>
    def get_training_file_url(self, obj):
        """
        This method is called by DRF to populate the 'training_file_url' field.
        """
        if obj.training_file and hasattr(obj.training_file, 'url'):
            request = self.context.get('request')
            # This part is correct, it looks up your named URL
            serve_url = reverse('serve-han-material-file', kwargs={'pk': obj.pk})
            # This part is correct, it builds the full URL
            return request.build_absolute_uri(serve_url)
        return None



# --- MODIFIED SUBTOPIC SERIALIZER ---
class HanSubtopicSerializer(serializers.ModelSerializer):
    materials = HanTrainingContentSerializer(many=True, read_only=True)

    class Meta:
        model = HanSubtopic
        # We must include 'han_content' so it can be sent in a POST request.
        fields = ['id', 'title', 'materials', 'han_content']
        extra_kwargs = {'han_content': {'write_only': True}}



#  Main Topic Serializers ---

class HanContentDetailSerializer(serializers.ModelSerializer):
    """
    Serializes a SINGLE Main Topic with its full nested structure of subtopics and materials.
    This is used for the "detail" view (e.g., GET /api/han-content/1/).
    """
    # The 'subtopics' field matches the `related_name` in the HanSubtopic model.
    subtopics = HanSubtopicSerializer(many=True, read_only=True)

    class Meta:
        model = HanContent
        fields = ['id', 'title', 'subtopics']


class HanContentListSerializer(serializers.ModelSerializer):
    """
    Serializes a Main Topic for a list view.
    It's lightweight and only includes the essential info.
    This is used for the "list" view (e.g., GET /api/han-content/).
    """
    class Meta:
        model = HanContent
        fields = ['id', 'title']





from django.urls import reverse
from rest_framework import serializers
from .models import ShoContent, ShoSubtopic, ShoTrainingContent


# --- THIS IS THE CORRECTED SHO SERIALIZER ---
class ShoTrainingContentSerializer(serializers.ModelSerializer):
    # This field accepts the file during an upload (POST/PUT).
    training_file = serializers.FileField(write_only=True, required=False)

    # This field is what your React frontend will receive.
    training_file_url = serializers.SerializerMethodField(read_only=True)

    # RENAMED for consistency with the Han serializer and the React frontend.
    # The frontend expects 'description', not 'sho_description'.
    description = serializers.CharField(source='sho_description')

    class Meta:
        model = ShoTrainingContent
        # Updated the fields list to be consistent and correct.
        fields = [
            'id',
            'description',          # Using the renamed field
            'training_file',        # For uploads
            'training_file_url',    # For downloads
            'url_link',
            'sho_subtopic'
        ]
        extra_kwargs = {'sho_subtopic': {'write_only': True}}

    # The method to generate the URL for the 'training_file_url' field.
    def get_training_file_url(self, obj):
        """
        Populates the 'training_file_url' field.
        """
        if obj.training_file and hasattr(obj.training_file, 'url'):
            request = self.context.get('request')
            # This correctly looks up the specific URL for Shokuchou files.
            serve_url = reverse('serve-sho-material-file', kwargs={'pk': obj.pk})
            return request.build_absolute_uri(serve_url)
        return None




# --- SHO SUBTOPIC SERIALIZER ---
class ShoSubtopicSerializer(serializers.ModelSerializer):
    sho_materials = ShoTrainingContentSerializer(many=True, read_only=True)

    class Meta:
        model = ShoSubtopic
        fields = ['id', 'title', 'sho_materials', 'sho_content']
        extra_kwargs = {'sho_content': {'write_only': True}}


# --- SHO CONTENT DETAIL SERIALIZER ---
class ShoContentDetailSerializer(serializers.ModelSerializer):
    # Nested subtopics with materials
    sho_subtopics = ShoSubtopicSerializer(many=True, read_only=True)

    class Meta:
        model = ShoContent
        fields = ['id', 'title', 'sho_subtopics']


# --- SHO CONTENT LIST SERIALIZER ---
class ShoContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoContent
        fields = ['id', 'title']



# hanchouend

# ----------------------ojtlistingserializer---------------------#


from rest_framework import serializers
from django.db.models import Sum
from .models import (
    LevelTwoTraineeInfo, LevelTwoOJTScore,
    LevelTwoQATraineeInfo, LevelTwoQAOJTScore
)



class UnifiedOJTStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    traineeId = serializers.CharField(read_only=True)
    trainee_name = serializers.CharField(read_only=True)
    trainer_name = serializers.CharField(read_only=True)

    # ✅ Shared computed fields
    production_or_quality = serializers.SerializerMethodField()
    line = serializers.SerializerMethodField()
    station = serializers.SerializerMethodField()
    daysCompleted = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    rawScore = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    # 🔹 Unified Production/Quality name
    def get_production_or_quality(self, obj):
        if isinstance(obj, LevelTwoTraineeInfo):  # Production trainee
            return obj.line.production.name if obj.line and obj.line.production else None
        elif isinstance(obj, LevelTwoQATraineeInfo):  # QA trainee
            return obj.line.quality.name if obj.line and obj.line.quality else None
        return None

    def get_line(self, obj):
        if isinstance(obj, LevelTwoTraineeInfo):
            return obj.line.name if obj.line else None
        elif isinstance(obj, LevelTwoQATraineeInfo):
            return obj.line.name if obj.line else None
        return None

    # def get_station(self, obj):
    #     if isinstance(obj, LevelTwoTraineeInfo):
    #         return obj.station.name if obj.station else None
    #     elif isinstance(obj, LevelTwoQATraineeInfo):
    #         return None  # QA has no station
    #     return None
    def get_station(self, obj):
        if isinstance(obj, LevelTwoTraineeInfo):
            return obj.station.name if obj.station else None
        elif isinstance(obj, LevelTwoQATraineeInfo):
            return obj.station.name if obj.station else None   # ✅ FIXED
        return None

    def get_score_model(self, obj):
        if isinstance(obj, LevelTwoTraineeInfo):
            return LevelTwoOJTScore
        elif isinstance(obj, LevelTwoQATraineeInfo):
            return LevelTwoQAOJTScore
        return None

    def get_daysCompleted(self, obj):
        ScoreModel = self.get_score_model(obj)
        return (
            ScoreModel.objects
            .filter(trainee=obj)
            .exclude(score=0)
            .values("day")
            .distinct()
            .count()
        )

    def get_rawScore(self, obj):
        ScoreModel = self.get_score_model(obj)
        return (
            ScoreModel.objects
            .filter(trainee=obj)
            .exclude(score=0)
            .aggregate(total=Sum("score"))["total"]
            or 0
        )

    def get_score(self, obj):
        return self.get_rawScore(obj)

    def get_status(self, obj):
        return "Complete" if self.get_daysCompleted(obj) == 6 else "Incomplete"

    def get_result(self, obj):
        ScoreModel = self.get_score_model(obj)
        days = self.get_daysCompleted(obj)
        if days < 6:
            return "N/A"

        scores = ScoreModel.objects.filter(trainee=obj).exclude(score=0)
        if scores.filter(score__lt=10).exists():
            return "Fail"

        return "Pass"

    def get_category(self, obj):
        if isinstance(obj, LevelTwoTraineeInfo):
            return "Production"
        elif isinstance(obj, LevelTwoQATraineeInfo):
            return "Quality"
        return "Unknown"

    def get_level(self, obj):
        if isinstance(obj, LevelTwoQATraineeInfo):
            return "Level 2 - QA"
        elif isinstance(obj, LevelTwoTraineeInfo):
            return "Level 2 - Production"
        return "Unknown"
    

    
from rest_framework import serializers
from django.db.models import Sum
from .models import (
    LevelThreeTraineeInfo, LevelThreeOJTScore,
    LevelThreeQATraineeInfo, LevelThreeQAOJTScore,
)


class UnifiedLevelThreeOJTStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    traineeId = serializers.CharField(source="trainee_Id", read_only=True)
    trainee_name = serializers.CharField(read_only=True)
    trainer_name = serializers.CharField(read_only=True)

    # Computed fields
    production_or_quality = serializers.SerializerMethodField()
    line = serializers.SerializerMethodField()
    station = serializers.SerializerMethodField()
    daysCompleted = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    rawScore = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    # 🔹 Production/Quality source name
    def get_production_or_quality(self, obj):
        if isinstance(obj, LevelThreeTraineeInfo):  # Production
            return obj.line.production.name if obj.line and obj.line.production else None
        elif isinstance(obj, LevelThreeQATraineeInfo):  # QA
            return obj.line.quality.name if obj.line and obj.line.quality else None
        return None

    def get_line(self, obj):
        return obj.line.name if obj.line else None

    def get_station(self, obj):
        if isinstance(obj, LevelThreeTraineeInfo):
            return obj.station.name if obj.station else None
        return None  # QA has no station

    def get_score_model(self, obj):
        if isinstance(obj, LevelThreeTraineeInfo):
            return LevelThreeOJTScore
        elif isinstance(obj, LevelThreeQATraineeInfo):
            return LevelThreeQAOJTScore
        return None

    def get_daysCompleted(self, obj):
        ScoreModel = self.get_score_model(obj)
        return (
            ScoreModel.objects
            .filter(trainee=obj)
            .exclude(score=0)
            .values("day")
            .distinct()
            .count()
        )

    def get_rawScore(self, obj):
        ScoreModel = self.get_score_model(obj)
        return (
            ScoreModel.objects
            .filter(trainee=obj)
            .exclude(score=0)
            .aggregate(total=Sum("score"))["total"]
            or 0
        )

    def get_score(self, obj):
        return self.get_rawScore(obj)

    def get_status(self, obj):
        return "Complete" if self.get_daysCompleted(obj) == 6 else "Incomplete"

    def get_result(self, obj):
        ScoreModel = self.get_score_model(obj)
        days = self.get_daysCompleted(obj)
        if days < 6:
            return "N/A"

        scores = ScoreModel.objects.filter(trainee=obj).exclude(score=0)
        if scores.filter(score__lt=10).exists():
            return "Fail"

        return "Pass"

    def get_category(self, obj):
        if isinstance(obj, LevelThreeTraineeInfo):
            return "Production"
        elif isinstance(obj, LevelThreeQATraineeInfo):
            return "Quality"
        return "Unknown"

    def get_level(self, obj):
        if isinstance(obj, LevelThreeQATraineeInfo):
            return "Level 3 - QA"
        elif isinstance(obj, LevelThreeTraineeInfo):
            return "Level 3 - Production"
        return "Unknown"









from rest_framework import serializers
from .models import FactoryStructure, ShopFloor, LineStructure, StationStructure

class StationStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationStructure
        fields = ['id', 'station_name']  # Updated from 'name'

class LineStructureSerializer(serializers.ModelSerializer):
    stations = StationStructureSerializer(many=True)

    class Meta:
        model = LineStructure
        fields = ['id', 'line_name', 'stations']  # Updated from 'name'

class ShopFloorSerializer(serializers.ModelSerializer):
    lines = LineStructureSerializer(many=True)

    class Meta:
        model = ShopFloor
        fields = ['id', 'shopfloor_name', 'lines']  # Updated from 'name'

class FactoryStructureSerializer(serializers.ModelSerializer):
    shop_floors = ShopFloorSerializer(many=True)

    class Meta:
        model = FactoryStructure
        fields = ['id', 'factory_name', 'shop_floors']  # Updated from 'name'

    def create(self, validated_data):
        shop_floors_data = validated_data.pop('shop_floors')
        factory = FactoryStructure.objects.create(**validated_data)
        for shop_floor_data in shop_floors_data:
            lines_data = shop_floor_data.pop('lines')
            shop_floor = ShopFloor.objects.create(factory_structure=factory, **shop_floor_data)
            for line_data in lines_data:
                stations_data = line_data.pop('stations')
                line = LineStructure.objects.create(shop_floor=shop_floor, **line_data)
                for station_data in stations_data:
                    StationStructure.objects.create(line=line, **station_data)
        return factory




from rest_framework import serializers
from .models import ProductionPlan

class ProductionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionPlan
        fields = '__all__'


# In your app's serializers.py file

from rest_framework import serializers
from .models import DailyProductionData

# In your serializers.py

from rest_framework import serializers
from .models import DailyProductionData # ### KEY CHANGE: Import the new model ###

# ... your existing ProductionPlanSerializer can remain for now ...

class DailyProductionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProductionData
        fields = '__all__'

from rest_framework import serializers
from .models import NewFactory, NewDepartment, NewLine, NewWorkstation

class NewFactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewFactory
        fields = '__all__'

class NewDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewDepartment
        fields = '__all__'

class NewLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewLine
        fields = '__all__'

class NewWorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewWorkstation
        fields = '__all__'






# # ==================== NOTIFICATION SERIALIZERS ====================

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.SerializerMethodField()
    operator_name = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    is_recent = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 'recipient',
            'recipient_name', 'recipient_email', 'operator', 'operator_name',
            'level', 'level_name', 'training_schedule', 'is_read', 'is_sent',
            'read_at', 'created_at', 'sent_at', 'metadata', 'priority',
            'time_ago', 'is_recent'
        ]
        read_only_fields = ['id', 'created_at', 'sent_at', 'time_ago', 'is_recent']

    def get_recipient_name(self, obj):
        """Get recipient's full name"""
        if obj.recipient:
            return f"{obj.recipient.first_name} {obj.recipient.last_name}".strip()
        return None

    def get_operator_name(self, obj):
        """Get operator's name from EmployeeMaster"""
        if obj.operator:
            return obj.operator.name
        return None

    def get_level_name(self, obj):
        """Get level name (adjust depending on your Level model)"""
        if obj.level:
            # if Level has 'name' field
            return getattr(obj.level, "name", None)
        return None

    def get_time_ago(self, obj):
        """Get human-readable time difference"""
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.created_at

        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

    def get_is_recent(self, obj):
        """Check if notification is recent (within last 24 hours)"""
        from django.utils import timezone
        from datetime import timedelta
        return obj.created_at > timezone.now() - timedelta(hours=24)


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'title', 'message', 'notification_type', 'recipient',
            'recipient_email', 'operator', 'level', 'training_schedule',
            'priority', 'metadata'
        ]

    def validate(self, data):
        if not data.get('recipient') and not data.get('recipient_email'):
            raise serializers.ValidationError(
                "Either recipient or recipient_email must be specified."
            )
        return data


class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read', 'read_at']

    def update(self, instance, validated_data):
        if 'is_read' in validated_data:
            if validated_data['is_read'] and not instance.is_read:
                instance.mark_as_read()
            elif not validated_data['is_read'] and instance.is_read:
                instance.mark_as_unread()
        return instance


class NotificationStatsSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()
    unread_count = serializers.IntegerField()
    read_count = serializers.IntegerField()
    recent_count = serializers.IntegerField()
    by_type = serializers.DictField()
    by_priority = serializers.DictField()


# # end
