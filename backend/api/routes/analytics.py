from fastapi import APIRouter, HTTPException
import json
# Assuming predictive_models.py is in the same directory or appropriately structured
try:
    from ...analytics.predictive_models import PredictiveAnalytics
except ImportError:
    from analytics.predictive_models import PredictiveAnalytics

router = APIRouter()

# Initialize the predictive analytics model
predictive_analytics = PredictiveAnalytics()

@router.get('/predictive/cost-trend')
async def get_cost_trend(future_days: int = 7):
    """
    Get predicted cost trends for the specified number of future days.
    For now, uses mock data. In a full implementation, this would use real historical data.
    """
    # Mock historical data - in a real app, this would come from a database
    try:
        with open('frontend/src/components/analytics/mockData.js', 'r') as file:
            mock_data_str = file.read()
            # Extract the array from the export statement
            start_idx = mock_data_str.find('[')
            end_idx = mock_data_str.rfind(']') + 1
            mock_data_json = mock_data_str[start_idx:end_idx]
            historical_data = json.loads(mock_data_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading mock data: {str(e)}")

    # Check if model is trained, if not, train it with historical data
    if not predictive_analytics.is_trained:
        success, message = predictive_analytics.train_model(historical_data, target_column='cost')
        if not success:
            raise HTTPException(status_code=500, detail=f"Model training failed: {message}")

    # Get predictions
    predictions, message = predictive_analytics.predict_trend(historical_data, future_days=future_days)
    if predictions is None:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {message}")

    return {'predictions': predictions, 'message': message}

@router.get('/predictive/pattern-analysis')
async def get_pattern_analysis():
    """
    Analyze historical data for patterns and anomalies.
    For now, uses mock data. In a full implementation, this would use real historical data.
    """
    # Mock historical data - in a real app, this would come from a database
    try:
        with open('frontend/src/components/analytics/mockData.js', 'r') as file:
            mock_data_str = file.read()
            # Extract the array from the export statement
            start_idx = mock_data_str.find('[')
            end_idx = mock_data_str.rfind(']') + 1
            mock_data_json = mock_data_str[start_idx:end_idx]
            historical_data = json.loads(mock_data_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading mock data: {str(e)}")

    # Analyze patterns
    analysis_results, message = predictive_analytics.analyze_patterns(historical_data)
    if analysis_results is None:
        raise HTTPException(status_code=500, detail=f"Pattern analysis failed: {message}")

    return {'analysis': analysis_results, 'message': message}

@router.get('/analytics/custom-report')
async def get_custom_report(type: str = 'cost'):
    """
    Get custom analytics report based on the specified type.
    For now, uses mock data. In a full implementation, this would use real historical data.
    """
    # Mock historical data - in a real app, this would come from a database
    try:
        with open('frontend/src/components/analytics/mockData.js', 'r') as file:
            mock_data_str = file.read()
            # Extract the array from the export statement
            start_idx = mock_data_str.find('[')
            end_idx = mock_data_str.rfind(']') + 1
            mock_data_json = mock_data_str[start_idx:end_idx]
            historical_data = json.loads(mock_data_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading mock data: {str(e)}")

    return {'reports': historical_data, 'message': f"Custom {type} report retrieved successfully"}
