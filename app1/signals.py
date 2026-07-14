# """
# Django signals for automatic notification generation
# Handles real-time notification triggers for various system events
# """

# from django.db.models.signals import post_save, post_delete, pre_save
# from django.dispatch import receiver
# from django.utils import timezone
# from django.contrib.auth import get_user_model
# from .models import (
#     Notification, OperatorMaster, Test, OperatorTestAssignment,
#     OperatorSkillLevel, MachineAllocation, TrainingContent,
#     LevelTwoTrainingContent, Schedule, OperatorPerformanceEvaluation,
#     MultiSkilling, User
# )
# from .consumers import broadcast_notification_to_user, broadcast_notification_count_to_user

# User = get_user_model()


# def create_notification(title, message, notification_type, recipient=None,
#                        recipient_email=None, operator=None, level=None,
#                        training_schedule=None, priority='medium', metadata=None):
#     """
#     Helper function to create notifications with real-time broadcasting
#     """
#     notification = Notification.objects.create(
#         title=title,
#         message=message,
#         notification_type=notification_type,
#         recipient=recipient,
#         recipient_email=recipient_email,
#         operator=operator,
#         level=level,
#         training_schedule=training_schedule,
#         priority=priority,
#         metadata=metadata or {}
#     )

#     # Broadcast notification in real-time if recipient exists
#     if recipient:
#         from .serializers import NotificationSerializer
#         serializer = NotificationSerializer(notification)
#         broadcast_notification_to_user(recipient.id, serializer.data)

#         # Update notification count
#         unread_count = Notification.objects.filter(
#             recipient=recipient, is_read=False
#         ).count()
#         broadcast_notification_count_to_user(recipient.id, unread_count)

#     return notification


# def get_admin_users():
#     """Get all admin users for system notifications"""
#     admin_users = User.objects.filter(role__in=['admin', 'management'])
#     # If no admin users found, notify all users for testing
#     if not admin_users.exists():
#         return User.objects.all()[:5]  # Limit to first 5 users to avoid spam
#     return admin_users


# @receiver(post_save, sender=OperatorMaster)
# def notify_employee_registration(sender, instance, created, **kwargs):
#     """Notify when a new employee is registered"""
#     try:
#         if created:
#             admin_users = get_admin_users()
#             for admin in admin_users:
#                 create_notification(
#                     title="New Employee Registered",
#                     message=f"New employee {instance.full_name} (ID: {instance.employee_code}) has been registered in the system.",
#                     notification_type='employee_registration',
#                     recipient=admin,
#                     operator=instance,
#                     priority='medium',
#                     metadata={
#                         'employee_code': instance.employee_code,
#                         'department': instance.department,
#                         'designation': instance.designation,
#                         'auto_generated': True
#                     }
#                 )
#     except Exception as e:
#         print(f"❌ Error creating employee registration notification: {str(e)}")


# # @receiver(post_save, sender=OperatorTestAssignment)
# # def notify_test_assignment(sender, instance, created, **kwargs):
# #     """Notify when a test is assigned to an operator"""
# #     if created:
# #         admin_users = get_admin_users()
# #         for admin in admin_users:
# #             create_notification(
# #                 title="Test Assigned",
# #                 message=f"Test '{instance.test.test_name}' has been assigned to {instance.operator.full_name}.",
# #                 notification_type='test_assigned',
# #                 recipient=admin,
# #                 operator=instance.operator,
# #                 priority='medium',
# #                 metadata={
# #                     'test_name': instance.test.test_name,
# #                     'assigned_date': instance.assigned_on.isoformat()
# #                 }
# #             )


# # @receiver(post_save, sender=OperatorSkillLevel)
# # def notify_exam_completion(sender, instance, created, **kwargs):
# #     """Notify when an operator completes an exam or evaluation"""
# #     try:
# #         if not created and instance.status in ['Pass', 'Fail']:
# #             admin_users = get_admin_users()
# #             for admin in admin_users:
# #                 create_notification(
# #                     title="Level Exam Completed",
# #                     message=f"{instance.operator.full_name} has completed {instance.level.get_name_display()} evaluation with status: {instance.status}.",
# #                     notification_type='level_exam_completed',
# #                     recipient=admin,
# #                     operator=instance.operator,
# #                     level=instance.level,
# #                     priority='high' if instance.status == 'Fail' else 'medium',
# #                     metadata={
# #                         'status': instance.status,
# #                         'written_score': getattr(instance, 'written_test_score', None),
# #                         'practical_score': getattr(instance, 'practical_test_score', None),
# #                         'observation_score': getattr(instance, 'observation_score', None),
# #                         'auto_generated': True
# #                     }
# #                 )
# #     except Exception as e:
# #         print(f"❌ Error creating exam completion notification: {str(e)}")


# # @receiver(post_save, sender=TrainingContent)
# # def notify_training_content_added(sender, instance, created, **kwargs):
# #     """Notify when new training content is added"""
# #     if created:
# #         admin_users = get_admin_users()
# #         for admin in admin_users:
# #             create_notification(
# #                 title="Bending Training Added",
# #                 message=f"New bending training content has been added for {instance.subtopic_content.title}.",
# #                 notification_type='bending_training_added',  # Updated to match your specification
# #                 recipient=admin,
# #                 priority='low',
# #                 metadata={
# #                     'content_type': 'Level 1',
# #                     'subtopic': instance.subtopic_content.title
# #                 }
# #             )


# # @receiver(post_save, sender=LevelTwoTrainingContent)
# # def notify_level2_training_content_added(sender, instance, created, **kwargs):
# #     """Notify when new Level 2 training content is added"""
# #     if created:
# #         admin_users = get_admin_users()
# #         for admin in admin_users:
# #             create_notification(
# #                 title="Bending Training Added",
# #                 message=f"New Level 2 bending training content has been added for {instance.subunit.title}.",
# #                 notification_type='bending_training_added',  # Updated to match your specification
# #                 recipient=admin,
# #                 priority='low',
# #                 metadata={
# #                     'content_type': 'Level 2',
# #                     'subunit': instance.subunit.title
# #                 }
# #             )


# @receiver(post_save, sender=Schedule)
# def notify_training_scheduled(sender, instance, created, **kwargs):
#     """Notify when training is scheduled or rescheduled"""
#     try:
#         if created:
#             admin_users = get_admin_users()
#             for admin in admin_users:
#                 # Get training name and venue safely
#                 training_name = str(instance.training_name) if instance.training_name else "Training"
#                 venue_name = instance.venue.name if instance.venue else "TBD"

#                 # Check if this is refresher training based on training name
#                 is_refresher = 'refresher' in training_name.lower()

#                 # Get employee count for the message
#                 employee_count = instance.employees.count() if hasattr(instance, 'employees') else 0

#                 if is_refresher:
#                     create_notification(
#                         title="Refresher Training Scheduled",
#                         message=f"Refresher training '{training_name}' has been scheduled for {employee_count} employees on {instance.date} at {instance.time}.",
#                         notification_type='refresher_training_scheduled',
#                         recipient=admin,
#                         training_schedule=instance,
#                         priority='medium',
#                         metadata={
#                             'date': instance.date.isoformat() if instance.date else None,
#                             'time': instance.time.isoformat() if instance.time else None,
#                             'venue': venue_name,
#                             'training_name': training_name,
#                             'employee_count': employee_count,
#                             'training_type': 'refresher',
#                             'auto_generated': True
#                         }
#                     )
#                 else:
#                     create_notification(
#                         title="Training Scheduled",
#                         message=f"Training session '{training_name}' has been scheduled for {employee_count} employees on {instance.date} at {instance.time}.",
#                         notification_type='training_reschedule',
#                         recipient=admin,
#                         training_schedule=instance,
#                         priority='medium',
#                         metadata={
#                             'date': instance.date.isoformat() if instance.date else None,
#                             'time': instance.time.isoformat() if instance.time else None,
#                             'venue': venue_name,
#                             'training_name': training_name,
#                             'employee_count': employee_count,
#                             'auto_generated': True
#                         }
#                     )
#         else:
#             # Check if status changed to completed
#             if hasattr(instance, 'status') and instance.status == 'completed':
#                 admin_users = get_admin_users()
#                 for admin in admin_users:
#                     training_name = str(instance.training_name) if instance.training_name else "Training"
#                     is_refresher = 'refresher' in training_name.lower()
#                     employee_count = instance.employees.count() if hasattr(instance, 'employees') else 0

#                     if is_refresher:
#                         create_notification(
#                             title="Refresher Training Completed",
#                             message=f"Refresher training '{training_name}' has been completed by {employee_count} employees.",
#                             notification_type='refresher_training_completed',
#                             recipient=admin,
#                             training_schedule=instance,
#                             priority='medium',
#                             metadata={
#                                 'training_name': training_name,
#                                 'employee_count': employee_count,
#                                 'training_type': 'refresher',
#                                 'auto_generated': True
#                             }
#                         )
#                     else:
#                         create_notification(
#                             title="Training Completed",
#                             message=f"Training session '{training_name}' has been completed by {employee_count} employees.",
#                             notification_type='training_reschedule',
#                             recipient=admin,
#                             training_schedule=instance,
#                             priority='medium',
#                             metadata={
#                                 'training_name': training_name,
#                                 'employee_count': employee_count,
#                                 'auto_generated': True
#                             }
#                         )
#     except Exception as e:
#         # Log the error but don't break the schedule creation
#         print(f"❌ Error creating training notification: {str(e)}")
#         # Don't re-raise the exception to avoid breaking schedule creation


# # @receiver(post_save, sender=MachineAllocation)
# # def notify_machine_allocation(sender, instance, created, **kwargs):
# #     """Notify when a machine is allocated to an operator"""
# #     if created:
# #         admin_users = get_admin_users()
# #         for admin in admin_users:
# #             create_notification(
# #                 title="Machine Allocated",
# #                 message=f"Machine '{instance.machine.name}' has been allocated to {instance.employee.full_name}.",
# #                 notification_type='machine_allocated',
# #                 recipient=admin,
# #                 operator=instance.employee,
# #                 priority='medium',
# #                 metadata={
# #                     'machine_name': instance.machine.name,
# #                     'machine_level': instance.machine.level,
# #                     'approval_status': instance.approval_status
# #                 }
# #             )


# # @receiver(post_save, sender=MultiSkilling)
# # def notify_multiskilling_update(sender, instance, created, **kwargs):
# #     """Notify when multi-skilling status is updated"""
# #     if not created and instance.status in ['completed', 'rescheduled']:
# #         admin_users = get_admin_users()
# #         for admin in admin_users:
# #             create_notification(
# #                 title="Multi-Skilling Update",
# #                 message=f"Multi-skilling status for {instance.employee.full_name} has been updated to {instance.status}.",
# #                 notification_type='skill_matrix_updated',
# #                 recipient=admin,
# #                 operator=instance.employee,
# #                 priority='medium',
# #                 metadata={
# #                     'status': instance.status,
# #                     'skill_level': instance.skill_level,
# #                     'department': instance.department.department if hasattr(instance.department, 'department') else str(instance.department)
# #                 }
# #             )


# # @receiver(post_save, sender=OperatorPerformanceEvaluation)
# # def notify_evaluation_completed(sender, instance, created, **kwargs):
# #     """Notify when operator performance evaluation is completed"""
# #     if created:
# #         admin_users = get_admin_users()
# #         for admin in admin_users:
# #             create_notification(
# #                 title="Performance Evaluation Created",
# #                 message=f"Performance evaluation has been created for {instance.cc_no.full_name}.",
# #                 notification_type='evaluation_completed',
# #                 recipient=admin,
# #                 operator=instance.cc_no,
# #                 priority='medium',
# #                 metadata={
# #                     'evaluation_date': instance.date.isoformat(),
# #                     'line': instance.line,
# #                     'process': instance.process_name
# #                 }
# #             )


# # Signal to clean up old notifications (optional)
# @receiver(post_save, sender=Notification)
# def cleanup_old_notifications(sender, instance, created, **kwargs):
#     """Clean up old notifications to prevent database bloat"""
#     if created:
#         # Keep only last 100 notifications per user
#         if instance.recipient:
#             old_notifications = Notification.objects.filter(
#                 recipient=instance.recipient
#             ).order_by('-created_at')[100:]
            
#             if old_notifications:
#                 Notification.objects.filter(
#                     id__in=[n.id for n in old_notifications]
#                 ).delete()




"""
Django signals for automatic notification generation
Handles real-time notification triggers for various system events
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import (
    Notification, EmployeeMaster,
    MachineAllocation, TrainingContent,
    Schedule, 
    MultiSkilling
)
from .consumers import broadcast_notification_to_user, broadcast_notification_count_to_user

User = get_user_model()


def create_notification(title, message, notification_type, recipient=None,
                       recipient_email=None, operator=None, level=None,
                       training_schedule=None, priority='medium', metadata=None):
    """
    Helper function to create notifications with real-time broadcasting
    """
    notification = Notification.objects.create(
        title=title,
        message=message,
        notification_type=notification_type,
        recipient=recipient,
        recipient_email=recipient_email,
        operator=operator,
        level=level,
        training_schedule=training_schedule,
        priority=priority,
        metadata=metadata or {}
    )

    # Broadcast notification in real-time if recipient exists
    if recipient:
        from .serializers import NotificationSerializer
        serializer = NotificationSerializer(notification)
        broadcast_notification_to_user(recipient.id, serializer.data)

        # Update notification count
        unread_count = Notification.objects.filter(
            recipient=recipient, is_read=False
        ).count()
        broadcast_notification_count_to_user(recipient.id, unread_count)

    return notification


def get_admin_users():
    """Get all admin users for system notifications"""
    admin_users = User.objects.filter(role__in=['admin', 'management'])
    # If no admin users found, notify all users for testing
    if not admin_users.exists():
        return User.objects.all()[:5]  # Limit to first 5 users to avoid spam
    return admin_users


@receiver(post_save, sender=EmployeeMaster)
def notify_employee_registration(sender, instance, created, **kwargs):
    """Notify when a new employee is registered"""
    try:
        if created:
            admin_users = get_admin_users()
            for admin in admin_users:
                create_notification(
                    title="New Employee Registered",
                    message=f"New employee {instance.name} (Pay Code: {instance.pay_code}) has been registered in the system.",
                    notification_type='employee_registration',
                    recipient=admin,
                    operator=None,  # EmployeeMaster is not directly an operator
                    priority='medium',
                    metadata={
                        'pay_code': instance.pay_code,
                        'card_no': instance.card_no,
                        'department': instance.department,
                        'section': instance.section,
                        'designation_category': instance.desig_category,
                        'joining_date': str(instance.joining_date),
                        'auto_generated': True
                    }
                )
    except Exception as e:
        print(f"❌ Error creating employee registration notification: {str(e)}")


@receiver(post_save, sender=Schedule)
def notify_training_scheduled(sender, instance, created, **kwargs):
    """Notify when training is scheduled or rescheduled"""
    try:
        if created:
            admin_users = get_admin_users()
            for admin in admin_users:
                training_name = str(instance.training_name) if instance.training_name else "Training"
                venue_name = instance.venue.name if instance.venue else "TBD"
                is_refresher = 'refresher' in training_name.lower()
                employee_count = instance.employees.count() if hasattr(instance, 'employees') else 0

                if is_refresher:
                    create_notification(
                        title="Refresher Training Scheduled",
                        message=f"Refresher training '{training_name}' has been scheduled for {employee_count} employees on {instance.date} at {instance.time}.",
                        notification_type='refresher_training_scheduled',
                        recipient=admin,
                        training_schedule=instance,
                        priority='medium',
                        metadata={
                            'date': instance.date.isoformat() if instance.date else None,
                            'time': instance.time.isoformat() if instance.time else None,
                            'venue': venue_name,
                            'training_name': training_name,
                            'employee_count': employee_count,
                            'training_type': 'refresher',
                            'auto_generated': True
                        }
                    )
                else:
                    create_notification(
                        title="Training Scheduled",
                        message=f"Training session '{training_name}' has been scheduled for {employee_count} employees on {instance.date} at {instance.time}.",
                        notification_type='training_reschedule',
                        recipient=admin,
                        training_schedule=instance,
                        priority='medium',
                        metadata={
                            'date': instance.date.isoformat() if instance.date else None,
                            'time': instance.time.isoformat() if instance.time else None,
                            'venue': venue_name,
                            'training_name': training_name,
                            'employee_count': employee_count,
                            'auto_generated': True
                        }
                    )
        else:
            # Notify if training is completed
            if hasattr(instance, 'status') and instance.status == 'completed':
                admin_users = get_admin_users()
                for admin in admin_users:
                    training_name = str(instance.training_name) if instance.training_name else "Training"
                    is_refresher = 'refresher' in training_name.lower()
                    employee_count = instance.employees.count() if hasattr(instance, 'employees') else 0

                    if is_refresher:
                        create_notification(
                            title="Refresher Training Completed",
                            message=f"Refresher training '{training_name}' has been completed by {employee_count} employees.",
                            notification_type='refresher_training_completed',
                            recipient=admin,
                            training_schedule=instance,
                            priority='medium',
                            metadata={
                                'training_name': training_name,
                                'employee_count': employee_count,
                                'training_type': 'refresher',
                                'auto_generated': True
                            }
                        )
                    else:
                        create_notification(
                            title="Training Completed",
                            message=f"Training session '{training_name}' has been completed by {employee_count} employees.",
                            notification_type='training_reschedule',
                            recipient=admin,
                            training_schedule=instance,
                            priority='medium',
                            metadata={
                                'training_name': training_name,
                                'employee_count': employee_count,
                                'auto_generated': True
                            }
                        )
    except Exception as e:
        print(f"❌ Error creating training notification: {str(e)}")

# Signal for Machine Allocation
@receiver(post_save, sender=MachineAllocation)
def notify_machine_allocation(sender, instance, created, **kwargs):
    if created:
        admins = get_admin_users()

        notification_message = (
            f"Machine '{instance.machine.name}' has been allocated to {instance.employee.name} "
            f"with status: {instance.get_approval_status_display()}"
        )

        # Notify Admins
        for admin in admins:
            create_notification(
                title="Machine Allocated",
                message=notification_message,
                notification_type='machine_allocated',
                recipient=admin,
                operator=instance.employee,
                priority='medium',
                metadata={
                    'machine': instance.machine.name,
                    'employee': instance.employee.name,
                    'approval_status': instance.approval_status,
                    'allocated_at': str(instance.allocated_at)
                }
            )

        # Optionally: Notify the employee (if linked to User model)
        try:
            user = User.objects.get(email=instance.employee.card_no)  # Or use another field
            create_notification(
                title="Machine Allocation Update",
                message=f"You have been assigned: {instance.machine.name}. Status: {instance.get_approval_status_display()}",
                notification_type='machine_allocated',
                recipient=user,
                operator=instance.employee,
                priority='low',
                metadata={
                    'machine': instance.machine.name,
                    'status': instance.approval_status
                }
            )
        except User.DoesNotExist:
            pass  # No linked user — skip

@receiver(post_save, sender=Notification)
def cleanup_old_notifications(sender, instance, created, **kwargs):
    """Clean up old notifications to prevent database bloat"""
    if created and instance.recipient:
        old_notifications = Notification.objects.filter(
            recipient=instance.recipient
        ).order_by('-created_at')[100:]

        if old_notifications:
            Notification.objects.filter(
                id__in=[n.id for n in old_notifications]
            ).delete()
