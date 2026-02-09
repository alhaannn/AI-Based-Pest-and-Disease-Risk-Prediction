"""
AI Prediction Engine for Pest and Disease Risk Assessment
Uses machine learning to predict outbreak risks based on historical data and environmental conditions
"""
import numpy as np
from datetime import timedelta
from django.utils import timezone
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import os


class PestRiskPredictor:
    """
    Machine Learning model for predicting pest/disease outbreak risks
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, crop, pest, weather_data, historical_records=None):
        """
        Extract and engineer features for prediction
        
        Features include:
        - Weather conditions (temperature, humidity, rainfall)
        - Crop characteristics (type, growth stage, area)
        - Pest characteristics (type, severity level)
        - Historical infestation patterns
        - Seasonal factors
        """
        features = []
        
        # Weather features (most recent 7 days average)
        if weather_data:
            avg_temp = np.mean([w.temperature_avg for w in weather_data])
            avg_humidity = np.mean([w.humidity for w in weather_data])
            total_rainfall = np.sum([w.rainfall for w in weather_data])
            avg_wind = np.mean([w.wind_speed for w in weather_data])
            
            # Weather risk indicators
            temp_risk = 1 if 20 <= avg_temp <= 30 else 0
            humidity_risk = 1 if avg_humidity > 70 else 0
            rainfall_risk = 1 if total_rainfall > 50 else 0
        else:
            avg_temp = avg_humidity = total_rainfall = avg_wind = 0
            temp_risk = humidity_risk = rainfall_risk = 0
        
        # Crop features
        crop_type_encoding = {
            'CEREAL': 1, 'VEGETABLE': 2, 'FRUIT': 3, 
            'LEGUME': 4, 'CASH_CROP': 5, 'OTHER': 6
        }
        crop_type_value = crop_type_encoding.get(crop.crop_type, 0)
        
        growth_stage_encoding = {
            'SEEDLING': 1, 'VEGETATIVE': 2, 'FLOWERING': 3,
            'FRUITING': 4, 'MATURITY': 5, 'HARVEST': 6
        }
        growth_stage_value = growth_stage_encoding.get(crop.growth_stage, 0)
        
        crop_area = float(crop.area) if crop.area else 0
        
        # Pest features
        pest_type_encoding = {
            'INSECT': 1, 'FUNGAL': 2, 'BACTERIAL': 3,
            'VIRAL': 4, 'WEED': 5, 'NEMATODE': 6, 'OTHER': 7
        }
        pest_type_value = pest_type_encoding.get(pest.pest_type, 0)
        
        severity_encoding = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4}
        pest_severity_value = severity_encoding.get(pest.severity_level, 0)
        
        # Historical pattern features
        if historical_records:
            recent_infestations = len([r for r in historical_records 
                                      if r.crop == crop and r.pest == pest])
            avg_historical_severity = np.mean([r.severity for r in historical_records]) if historical_records else 0
            days_since_last = 365  # Default if no history
            
            if historical_records:
                last_record = max(historical_records, key=lambda x: x.date)
                days_since_last = (timezone.now().date() - last_record.date).days
        else:
            recent_infestations = 0
            avg_historical_severity = 0
            days_since_last = 365
        
        # Seasonal features
        current_month = timezone.now().month
        is_monsoon = 1 if current_month in [6, 7, 8, 9] else 0
        is_winter = 1 if current_month in [12, 1, 2] else 0
        is_summer = 1 if current_month in [3, 4, 5] else 0
        
        # Combine all features
        features = [
            avg_temp,
            avg_humidity,
            total_rainfall,
            avg_wind,
            temp_risk,
            humidity_risk,
            rainfall_risk,
            crop_type_value,
            growth_stage_value,
            crop_area,
            pest_type_value,
            pest_severity_value,
            recent_infestations,
            avg_historical_severity,
            days_since_last,
            is_monsoon,
            is_winter,
            is_summer,
        ]
        
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data):
        """
        Train the model on historical infestation data
        
        training_data: list of tuples (features, risk_score)
        """
        if not training_data or len(training_data) < 10:
            # Not enough data to train
            return False
        
        X = np.array([item[0] for item in training_data])
        y = np.array([item[1] for item in training_data])
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest model
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        return True
    
    def predict(self, features):
        """
        Predict risk score for given features
        Returns: (risk_score, confidence)
        """
        if not self.is_trained:
            # Use rule-based prediction if model not trained
            return self._rule_based_prediction(features)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        risk_score = self.model.predict(features_scaled)[0]
        
        # Ensure score is between 0-100
        risk_score = max(0, min(100, risk_score))
        
        # Calculate confidence (simplified - based on feature strength)
        confidence = self._calculate_confidence(features)
        
        return risk_score, confidence
    
    def _rule_based_prediction(self, features):
        """
        Fallback rule-based prediction when ML model is not trained
        """
        features = features.flatten()
        
        # Extract key features
        avg_temp = features[0]
        avg_humidity = features[1]
        total_rainfall = features[2]
        temp_risk = features[4]
        humidity_risk = features[5]
        rainfall_risk = features[6]
        pest_severity = features[11]
        recent_infestations = features[12]
        avg_historical_severity = features[13]
        
        # Calculate risk score based on rules
        risk_score = 0
        
        # Weather contribution (40%)
        if temp_risk:
            risk_score += 15
        if humidity_risk:
            risk_score += 15
        if rainfall_risk:
            risk_score += 10
        
        # Pest severity contribution (30%)
        risk_score += pest_severity * 7.5
        
        # Historical pattern contribution (30%)
        if recent_infestations > 0:
            risk_score += min(20, recent_infestations * 5)
        risk_score += avg_historical_severity * 2
        
        # Ensure within bounds
        risk_score = max(0, min(100, risk_score))
        
        # Confidence is lower for rule-based predictions
        confidence = 65
        
        return risk_score, confidence
    
    def _calculate_confidence(self, features):
        """
        Calculate prediction confidence based on data quality and feature strength
        """
        features = features.flatten()
        
        # Base confidence
        confidence = 70
        
        # Increase confidence if we have historical data
        if features[12] > 0:  # recent_infestations
            confidence += 10
        
        # Increase confidence if weather data is available
        if features[0] > 0:  # avg_temp
            confidence += 10
        
        # Decrease confidence if data is old
        days_since_last = features[14]
        if days_since_last > 180:
            confidence -= 10
        
        return max(50, min(95, confidence))
    
    def save_model(self, filepath):
        """Save trained model to file"""
        if self.is_trained:
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'scaler': self.scaler,
                    'is_trained': self.is_trained
                }, f)
    
    def load_model(self, filepath):
        """Load trained model from file"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
                self.is_trained = data['is_trained']
            return True
        return False


def generate_predictions_for_all_crops():
    """
    Generate risk predictions for all active crops and known pests
    """
    from crops.models import Crop, Pest, InfestationRecord
    from weather.models import WeatherData
    from predictions.models import RiskPrediction
    
    predictor = PestRiskPredictor()
    
    # Get recent weather data (last 7 days)
    last_week = timezone.now().date() - timedelta(days=7)
    recent_weather = list(WeatherData.objects.filter(date__gte=last_week).order_by('-date'))
    
    # Get all active crops
    crops = Crop.objects.all()
    pests = Pest.objects.all()
    
    predictions_created = 0
    
    for crop in crops:
        for pest in pests:
            # Get historical records for this crop-pest combination
            historical_records = list(InfestationRecord.objects.filter(
                crop=crop,
                pest=pest
            ).order_by('-date')[:10])
            
            # Prepare features
            features = predictor.prepare_features(
                crop=crop,
                pest=pest,
                weather_data=recent_weather,
                historical_records=historical_records
            )
            
            # Predict
            risk_score, confidence = predictor.predict(features)
            
            # Only create prediction if risk is significant or there's historical data
            if risk_score > 20 or historical_records:
                # Check if prediction already exists for today
                today = timezone.now().date()
                existing = RiskPrediction.objects.filter(
                    crop=crop,
                    pest=pest,
                    prediction_date=today
                ).first()
                
                if existing:
                    # Update existing prediction
                    existing.risk_score = risk_score
                    existing.confidence = confidence
                    existing.save()
                else:
                    # Create new prediction
                    RiskPrediction.objects.create(
                        crop=crop,
                        pest=pest,
                        risk_score=risk_score,
                        confidence=confidence,
                        prediction_date=today,
                        contributing_factors=f"Weather conditions, historical patterns, crop stage: {crop.growth_stage}"
                    )
                    predictions_created += 1
    
    return predictions_created
