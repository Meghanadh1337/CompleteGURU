from django.core.management.base import BaseCommand
from forum.models import ImprovementArea

class Command(BaseCommand):
    help = 'Creates the default resume improvement areas'

    def handle(self, *args, **kwargs):
        improvement_areas = [
            {
                'name': 'Resume Length',
                'description': 'The resume is too long and should be condensed to highlight key information.',
            },
            {
                'name': 'Formatting',
                'description': 'The resume formatting could be improved for better readability and visual appeal.',
            },
            {
                'name': 'Skills Section',
                'description': 'The skills section needs more relevant skills or better organization.',
            },
            {
                'name': 'Experience Details',
                'description': 'Work experiences should be more achievement-oriented rather than task-based.',
            },
            {
                'name': 'Education Section',
                'description': 'Education information could be improved or reorganized.',
            },
        ]
        
        created_count = 0
        for area in improvement_areas:
            obj, created = ImprovementArea.objects.get_or_create(
                name=area['name'],
                defaults={'description': area['description']}
            )
            if created:
                created_count += 1
                
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} improvement areas')
        )
