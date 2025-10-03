import React, { useState } from 'react';
import './FlowGenerator.css';

interface FlowFormData {
  routineName: string;
  description: string;
  timeLength: string;
  desiredPoses: string;
}

const FlowGenerator: React.FC = () => {
  const [formData, setFormData] = useState<FlowFormData>({
    routineName: '',
    description: '',
    timeLength: '',
    desiredPoses: ''
  });
  const [isGenerating, setIsGenerating] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);

    try {
      // TODO: Implement actual flow generation logic
      console.log('Generating flow with data:', formData);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // For now, just show success message
      alert('Flow generated successfully! (This is a placeholder)');
    } catch (error) {
      alert('Failed to generate flow. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="flow-generator">
      <div className="container">
        <div className="flow-header">
          <h1>Create Your Perfect Flow</h1>
          <p>Tell us what you're looking for and we'll create a personalized yoga routine just for you.</p>
        </div>

        <div className="flow-form-container">
          <form onSubmit={handleSubmit} className="flow-form">
            <div className="form-section">
              <h2>Basic Information</h2>
              
              <div className="form-group">
                <label htmlFor="routineName">Routine Name</label>
                <input
                  type="text"
                  id="routineName"
                  name="routineName"
                  value={formData.routineName}
                  onChange={handleChange}
                  placeholder="e.g., Morning Energizer, Evening Wind-Down"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="timeLength">Time Length</label>
                <select
                  id="timeLength"
                  name="timeLength"
                  value={formData.timeLength}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select duration</option>
                  <option value="10">10 minutes</option>
                  <option value="15">15 minutes</option>
                  <option value="20">20 minutes</option>
                  <option value="30">30 minutes</option>
                  <option value="45">45 minutes</option>
                  <option value="60">60 minutes</option>
                  <option value="90">90 minutes</option>
                </select>
              </div>
            </div>

            <div className="form-section">
              <h2>Customize Your Flow</h2>
              
              <div className="form-group">
                <label htmlFor="description">Describe what you want today's routine to be like</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="e.g., I want a gentle morning routine to wake up my body, focus on hip openers and gentle twists, something that energizes but doesn't exhaust me..."
                  rows={4}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="desiredPoses">Poses you really want to include (Optional) </label>
                <textarea
                  id="desiredPoses"
                  name="desiredPoses"
                  value={formData.desiredPoses}
                  onChange={handleChange}
                  placeholder="e.g., Downward Dog, Warrior II, Child's Pose, Pigeon Pose, Tree Pose..."
                  rows={3}
                />
                <small className="form-hint">Separate poses with commas. Leave empty if you want us to choose for you.</small>
              </div>
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="generate-button"
                disabled={isGenerating}
              >
                {isGenerating ? (
                  <>
                    <span className="spinner"></span>
                    Generating Your Flow...
                  </>
                ) : (
                  <>
                    ✨ Generate My Flow
                  </>
                )}
              </button>
            </div>
          </form>

          <div className="flow-preview">
            <h3>Flow Preview</h3>
            <div className="preview-card">
              <div className="preview-info">
                <h4>{formData.routineName || 'Your Routine Name'}</h4>
                <p><strong>Duration:</strong> {formData.timeLength ? `${formData.timeLength} minutes` : 'Select duration'}</p>
                {formData.description && (
                  <p><strong>Description:</strong> {formData.description}</p>
                )}
                {formData.desiredPoses && (
                  <p><strong>Desired Poses:</strong> {formData.desiredPoses}</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FlowGenerator;
