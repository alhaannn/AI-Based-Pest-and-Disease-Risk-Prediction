"""
Django management command to populate database with realistic Indian agricultural demo data.
Usage: python manage.py load_indian_demo_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from crops.models import Crop, Pest, InfestationRecord
from weather.models import WeatherData
from alerts.models import PreventiveMeasure
import random


class Command(BaseCommand):
    help = 'Loads realistic Indian agricultural demo data into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading demo data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            InfestationRecord.objects.all().delete()
            WeatherData.objects.all().delete()
            PreventiveMeasure.objects.all().delete()
            Crop.objects.all().delete()
            Pest.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))

        self.stdout.write(self.style.SUCCESS('Loading Indian agricultural demo data...'))
        
        # Load data
        pests = self.create_pests()
        crops = self.create_crops()
        self.create_weather_data()
        self.create_preventive_measures(pests)
        self.create_infestation_records(crops, pests)
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✓ Demo data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'\nCreated:'))
        self.stdout.write(self.style.SUCCESS(f'  • {len(pests)} Pests/Diseases'))
        self.stdout.write(self.style.SUCCESS(f'  • {len(crops)} Crops'))
        self.stdout.write(self.style.SUCCESS(f'  • 90 Weather Records (3 months)'))
        self.stdout.write(self.style.SUCCESS(f'  • {PreventiveMeasure.objects.count()} Preventive Measures'))
        self.stdout.write(self.style.SUCCESS(f'  • {InfestationRecord.objects.count()} Infestation Records'))
        self.stdout.write(self.style.SUCCESS('\nNext steps:'))
        self.stdout.write(self.style.SUCCESS('  1. Visit /predictions/generate/ to generate AI predictions'))
        self.stdout.write(self.style.SUCCESS('  2. Check /alerts/dashboard/ for alerts'))
        self.stdout.write(self.style.SUCCESS('  3. Explore /predictions/analytics/ for insights'))

    def create_pests(self):
        """Create common Indian agricultural pests and diseases"""
        self.stdout.write('Creating pests and diseases...')
        
        pests_data = [
            # Insects
            {
                'name': 'Brown Planthopper',
                'pest_type': 'INSECT',
                'description': 'Scientific name: Nilaparvata lugens. Symptoms: Yellowing and drying of leaves, hopper burn, stunted growth. Affects: Rice, Paddy',
                'severity_level': 'HIGH',
            },
            {
                'name': 'Bollworm',
                'pest_type': 'INSECT',
                'description': 'Scientific name: Helicoverpa armigera. Symptoms: Holes in bolls, damaged flowers, larvae feeding on buds. Affects: Cotton, Tomato, Chickpea',
                'severity_level': 'HIGH',
            },
            {
                'name': 'Aphids',
                'pest_type': 'INSECT',
                'description': 'Scientific name: Aphis gossypii. Symptoms: Curled leaves, sticky honeydew, stunted growth, yellowing. Affects: Wheat, Cotton, Vegetables',
                'severity_level': 'MEDIUM',
            },
            {
                'name': 'Stem Borer',
                'pest_type': 'INSECT',
                'description': 'Scientific name: Scirpophaga incertulas. Symptoms: Dead hearts, white ears, holes in stem, wilting. Affects: Rice, Sugarcane, Maize',
                'severity_level': 'HIGH',
            },
            {
                'name': 'Whitefly',
                'pest_type': 'INSECT',
                'description': 'Scientific name: Bemisia tabaci. Symptoms: Yellowing leaves, sooty mold, leaf curl, stunted growth. Affects: Cotton, Tomato, Chili',
                'severity_level': 'MEDIUM',
            },
            
            # Fungal Diseases
            {
                'name': 'Blast Disease',
                'pest_type': 'FUNGAL',
                'description': 'Scientific name: Magnaporthe oryzae. Symptoms: Diamond-shaped lesions, neck rot, panicle blast. Affects: Rice, Wheat',
                'severity_level': 'HIGH',
            },
            {
                'name': 'Powdery Mildew',
                'pest_type': 'FUNGAL',
                'description': 'Scientific name: Erysiphe cichoracearum. Symptoms: White powdery coating on leaves, stunted growth. Affects: Wheat, Pea, Mango',
                'severity_level': 'MEDIUM',
            },
            {
                'name': 'Late Blight',
                'pest_type': 'FUNGAL',
                'description': 'Scientific name: Phytophthora infestans. Symptoms: Dark water-soaked lesions, white mold, rapid decay. Affects: Potato, Tomato',
                'severity_level': 'HIGH',
            },
            {
                'name': 'Rust Disease',
                'pest_type': 'FUNGAL',
                'description': 'Scientific name: Puccinia graminis. Symptoms: Orange-brown pustules on leaves and stems. Affects: Wheat, Barley, Sugarcane',
                'severity_level': 'MEDIUM',
            },
            
            # Bacterial Diseases
            {
                'name': 'Bacterial Leaf Blight',
                'pest_type': 'BACTERIAL',
                'description': 'Scientific name: Xanthomonas oryzae. Symptoms: Water-soaked lesions, yellowing, wilting. Affects: Rice, Paddy',
                'severity_level': 'MEDIUM',
            },
            {
                'name': 'Bacterial Wilt',
                'pest_type': 'BACTERIAL',
                'description': 'Scientific name: Ralstonia solanacearum. Symptoms: Sudden wilting, vascular browning, plant death. Affects: Tomato, Potato, Brinjal',
                'severity_level': 'HIGH',
            },
            
            # Viral Diseases
            {
                'name': 'Yellow Mosaic Virus',
                'pest_type': 'VIRAL',
                'description': 'Scientific name: Mungbean Yellow Mosaic Virus. Symptoms: Yellow mosaic patterns, stunted growth, reduced yield. Affects: Mungbean, Urdbean, Soybean',
                'severity_level': 'HIGH',
            },
        ]
        
        pests = []
        for pest_data in pests_data:
            pest, created = Pest.objects.get_or_create(
                name=pest_data['name'],
                defaults=pest_data
            )
            pests.append(pest)
            if created:
                self.stdout.write(f'  ✓ Created: {pest.name}')
        
        return pests

    def create_crops(self):
        """Create diverse Indian crops across different regions"""
        self.stdout.write('\nCreating crops...')
        
        crops_data = [
            # Rice (Kharif - Monsoon)
            {
                'name': 'Basmati Rice - Punjab Field',
                'crop_type': 'CEREAL',
                'growth_stage': 'FLOWERING',
                'planting_date': date.today() - timedelta(days=75),
                'area_hectares': 5.5,
                'field_location': 'Ludhiana, Punjab'
            },
            {
                'name': 'Paddy - West Bengal',
                'crop_type': 'CEREAL',
                'growth_stage': 'VEGETATIVE',
                'planting_date': date.today() - timedelta(days=45),
                'area_hectares': 3.2,
                'field_location': 'Burdwan, West Bengal'
            },
            
            # Wheat (Rabi - Winter)
            {
                'name': 'Wheat - Haryana Farm',
                'crop_type': 'CEREAL',
                'growth_stage': 'MATURITY',
                'planting_date': date.today() - timedelta(days=120),
                'area_hectares': 8.0,
                'field_location': 'Karnal, Haryana'
            },
            {
                'name': 'Durum Wheat - MP',
                'crop_type': 'CEREAL',
                'growth_stage': 'FLOWERING',
                'planting_date': date.today() - timedelta(days=90),
                'area_hectares': 4.5,
                'field_location': 'Indore, Madhya Pradesh'
            },
            
            # Cotton
            {
                'name': 'Bt Cotton - Gujarat',
                'crop_type': 'OTHER',
                'growth_stage': 'FLOWERING',
                'planting_date': date.today() - timedelta(days=80),
                'area_hectares': 6.0,
                'field_location': 'Ahmedabad, Gujarat'
            },
            {
                'name': 'Cotton - Maharashtra',
                'crop_type': 'OTHER',
                'growth_stage': 'VEGETATIVE',
                'planting_date': date.today() - timedelta(days=60),
                'area_hectares': 5.0,
                'field_location': 'Nagpur, Maharashtra'
            },
            
            # Vegetables
            {
                'name': 'Tomato - Karnataka',
                'crop_type': 'VEGETABLE',
                'growth_stage': 'FRUITING',
                'planting_date': date.today() - timedelta(days=70),
                'area_hectares': 1.5,
                'field_location': 'Bangalore, Karnataka'
            },
            {
                'name': 'Potato - UP',
                'crop_type': 'VEGETABLE',
                'growth_stage': 'VEGETATIVE',
                'planting_date': date.today() - timedelta(days=55),
                'area_hectares': 2.8,
                'field_location': 'Agra, Uttar Pradesh'
            },
            {
                'name': 'Chili - Andhra Pradesh',
                'crop_type': 'VEGETABLE',
                'growth_stage': 'FLOWERING',
                'planting_date': date.today() - timedelta(days=65),
                'area_hectares': 2.0,
                'field_location': 'Guntur, Andhra Pradesh'
            },
            
            # Pulses
            {
                'name': 'Chickpea - Rajasthan',
                'crop_type': 'LEGUME',
                'growth_stage': 'FLOWERING',
                'planting_date': date.today() - timedelta(days=85),
                'area_hectares': 4.0,
                'field_location': 'Jaipur, Rajasthan'
            },
            {
                'name': 'Mungbean - Bihar',
                'crop_type': 'LEGUME',
                'growth_stage': 'VEGETATIVE',
                'planting_date': date.today() - timedelta(days=40),
                'area_hectares': 2.5,
                'field_location': 'Patna, Bihar'
            },
            
            # Sugarcane
            {
                'name': 'Sugarcane - Tamil Nadu',
                'crop_type': 'OTHER',
                'growth_stage': 'VEGETATIVE',
                'planting_date': date.today() - timedelta(days=150),
                'area_hectares': 7.5,
                'field_location': 'Coimbatore, Tamil Nadu'
            },
        ]
        
        crops = []
        for crop_data in crops_data:
            crop, created = Crop.objects.get_or_create(
                name=crop_data['name'],
                defaults=crop_data
            )
            crops.append(crop)
            if created:
                self.stdout.write(f'  ✓ Created: {crop.name}')
        
        return crops

    def create_weather_data(self):
        """Create 3 months of realistic Indian weather data for different regions"""
        self.stdout.write('\nCreating weather data (90 days)...')
        
        # Different regions with typical weather patterns
        regions = [
            {
                'location': 'Ludhiana, Punjab',
                'temp_range': (15, 32),  # Winter-Spring
                'humidity_range': (50, 75),
                'rainfall_prob': 0.15
            },
            {
                'location': 'Burdwan, West Bengal',
                'temp_range': (20, 35),  # Humid subtropical
                'humidity_range': (65, 90),
                'rainfall_prob': 0.25
            },
            {
                'location': 'Ahmedabad, Gujarat',
                'temp_range': (18, 38),  # Semi-arid
                'humidity_range': (40, 70),
                'rainfall_prob': 0.10
            },
            {
                'location': 'Bangalore, Karnataka',
                'temp_range': (16, 30),  # Pleasant climate
                'humidity_range': (55, 80),
                'rainfall_prob': 0.20
            },
            {
                'location': 'Coimbatore, Tamil Nadu',
                'temp_range': (20, 34),  # Tropical
                'humidity_range': (60, 85),
                'rainfall_prob': 0.18
            },
        ]
        
        start_date = date.today() - timedelta(days=90)
        
        for i in range(90):
            current_date = start_date + timedelta(days=i)
            
            for region in regions:
                # Simulate realistic daily temperature variation
                temp_min = random.uniform(region['temp_range'][0], region['temp_range'][0] + 8)
                temp_max = random.uniform(region['temp_range'][1] - 5, region['temp_range'][1])
                temp_avg = (temp_min + temp_max) / 2
                
                # Humidity
                humidity = random.randint(region['humidity_range'][0], region['humidity_range'][1])
                
                # Rainfall (realistic pattern)
                rainfall = 0
                if random.random() < region['rainfall_prob']:
                    rainfall = round(random.uniform(2, 50), 1)
                
                # Wind speed
                wind_speed = round(random.uniform(5, 25), 1)
                
                WeatherData.objects.create(
                    date=current_date,
                    location=region['location'],
                    temperature_min=round(temp_min, 1),
                    temperature_max=round(temp_max, 1),
                    temperature_avg=round(temp_avg, 1),
                    humidity=humidity,
                    rainfall=rainfall,
                    wind_speed=wind_speed
                )
        
        self.stdout.write(f'  ✓ Created 90 days of weather data for {len(regions)} regions')

    def create_preventive_measures(self, pests):
        """Create preventive measures for Indian agricultural context"""
        self.stdout.write('\nCreating preventive measures...')
        
        measures_data = {
            'Brown Planthopper': [
                ('Neem Oil Spray', 'Apply 5% neem oil solution every 10 days. Foliar spray method.', 'HIGH', 'Before flowering stage', '5ml/L water'),
                ('Remove Weed Hosts', 'Clear grassy weeds around field boundaries to eliminate alternate hosts.', 'MEDIUM', 'Throughout season', 'Manual removal'),
                ('Resistant Varieties', 'Plant BPH-resistant varieties like Swarna Sub1 or IR64.', 'HIGH', 'At planting', 'Seed selection'),
            ],
            'Bollworm': [
                ('Bt Cotton', 'Use Bt cotton varieties with built-in resistance to bollworm.', 'HIGH', 'At planting', 'Bt seeds'),
                ('Pheromone Traps', 'Install pheromone traps for monitoring and mass trapping.', 'MEDIUM', 'Before flowering', '15-20 traps/ha'),
                ('NPV Spray', 'Apply Nuclear Polyhedrosis Virus for biological control.', 'HIGH', 'At egg hatching', '250 LE/ha'),
            ],
            'Aphids': [
                ('Yellow Sticky Traps', 'Install yellow sticky traps for early detection and monitoring.', 'MEDIUM', 'Early growth stage', '10-15 traps/ha'),
                ('Soap Solution Spray', 'Spray soap solution to control aphid populations.', 'MEDIUM', 'At first appearance', '2% solution'),
                ('Encourage Ladybugs', 'Conserve natural predators like ladybugs and lacewings.', 'HIGH', 'Throughout season', 'Biological control'),
            ],
            'Blast Disease': [
                ('Tricyclazole Spray', 'Apply Tricyclazole fungicide at tillering to booting stage.', 'HIGH', 'Tillering to booting', '0.6 g/L'),
                ('Seed Treatment', 'Treat seeds with Carbendazim before sowing.', 'HIGH', 'Before sowing', '2 g/kg seed'),
                ('Balanced Fertilization', 'Avoid excessive nitrogen, use balanced NPK with potash.', 'MEDIUM', 'Throughout season', 'Soil application'),
            ],
            'Late Blight': [
                ('Mancozeb Spray', 'Apply Mancozeb fungicide every 7-10 days during vegetative stage.', 'HIGH', 'Vegetative stage', '2.5 g/L'),
                ('Proper Spacing', 'Maintain adequate spacing for air circulation (60cm x 20cm).', 'MEDIUM', 'At planting', 'Planting practice'),
                ('Remove Infected Plants', 'Immediately remove and destroy infected plants to prevent spread.', 'HIGH', 'As soon as detected', 'Manual removal'),
            ],
            'Whitefly': [
                ('Imidacloprid Spray', 'Apply Imidacloprid systemic insecticide.', 'HIGH', 'At first appearance', '0.3 ml/L'),
                ('Reflective Mulch', 'Use silver reflective mulch to repel whiteflies.', 'MEDIUM', 'At planting', 'Mulching'),
                ('Neem Cake Application', 'Apply neem cake to soil as organic control.', 'MEDIUM', 'Before planting', '250 kg/ha'),
            ],
        }
        
        for pest in pests:
            if pest.name in measures_data:
                for measure in measures_data[pest.name]:
                    PreventiveMeasure.objects.create(
                        pest=pest,
                        action=measure[0],
                        description=measure[1],
                        effectiveness=measure[2],
                        timing=measure[3],
                        dosage=measure[4]
                    )
                self.stdout.write(f'  ✓ Added {len(measures_data[pest.name])} measures for {pest.name}')

    def create_infestation_records(self, crops, pests):
        """Create historical infestation records"""
        self.stdout.write('\nCreating infestation records...')
        
        # Realistic pest-crop associations
        pest_crop_map = {
            'Brown Planthopper': ['Basmati Rice - Punjab Field', 'Paddy - West Bengal'],
            'Bollworm': ['Bt Cotton - Gujarat', 'Cotton - Maharashtra', 'Tomato - Karnataka', 'Chickpea - Rajasthan'],
            'Aphids': ['Wheat - Haryana Farm', 'Durum Wheat - MP', 'Cotton - Maharashtra'],
            'Stem Borer': ['Basmati Rice - Punjab Field', 'Sugarcane - Tamil Nadu'],
            'Whitefly': ['Bt Cotton - Gujarat', 'Tomato - Karnataka', 'Chili - Andhra Pradesh'],
            'Blast Disease': ['Basmati Rice - Punjab Field', 'Paddy - West Bengal'],
            'Powdery Mildew': ['Wheat - Haryana Farm', 'Durum Wheat - MP'],
            'Late Blight': ['Potato - UP', 'Tomato - Karnataka'],
            'Rust Disease': ['Wheat - Haryana Farm', 'Sugarcane - Tamil Nadu'],
            'Bacterial Leaf Blight': ['Basmati Rice - Punjab Field', 'Paddy - West Bengal'],
            'Bacterial Wilt': ['Tomato - Karnataka', 'Potato - UP'],
            'Yellow Mosaic Virus': ['Mungbean - Bihar'],
        }
        
        count = 0
        for pest in pests:
            if pest.name in pest_crop_map:
                for crop_name in pest_crop_map[pest.name]:
                    crop = next((c for c in crops if c.name == crop_name), None)
                    if crop:
                        # Create 2-4 historical records per pest-crop combination
                        num_records = random.randint(2, 4)
                        for i in range(num_records):
                            days_ago = random.randint(30, 180)
                            severity = random.randint(2, 5)  # Severity is 1-5 in model
                            area = round(random.uniform(0.5, float(crop.area_hectares) * 0.6), 2)
                            
                            treatments = [
                                'Neem oil spray applied. Severity reduced after treatment.',
                                'Chemical pesticide used. Monitoring for effectiveness.',
                                'Biological control agents released. Natural predators introduced.',
                                'Infected plants removed and destroyed. Field sanitized.',
                                'Fungicide spray applied at recommended dosage.',
                                'Crop rotation implemented for next season.',
                                'No treatment applied - monitoring only. Low severity detected.'
                            ]
                            
                            InfestationRecord.objects.create(
                                crop=crop,
                                pest=pest,
                                date=date.today() - timedelta(days=days_ago),
                                severity=severity,
                                area_affected=area,
                                notes=f'Detected during routine field inspection. {random.choice(treatments)}'
                            )
                            count += 1
        
        self.stdout.write(f'  ✓ Created {count} historical infestation records')
