import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { runPrediction } from '../../redux/predictSlice';

const PredictiveModeling = () => {
  const dispatch = useDispatch();
  const [inputData, setInputData] = useState('');
  const [result, setResult] = useState(null);
  
  const handleRunPrediction = () => {
    dispatch(runPrediction(inputData))
      .unwrap()
      .then(response => setResult(response))
      .catch(error => console.error('Prediction failed:', error));
  };

  return (
    <div className="predictive-modeling">
      <h2>Predictive Modeling Integration</h2>
      
      <div className="input-section">
        <textarea 
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          placeholder="Enter input data for prediction"
        />
        <button onClick={handleRunPrediction}>Run Prediction</button>
      </div>
      
      {result && (
        <div className="result-section">
          <h3>Prediction Results</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default PredictiveModeling;
