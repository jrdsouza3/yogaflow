from openai import OpenAI
import json
import os
from typing import Dict, List, Tuple

class LLMService:
    """Service for generating yoga flows using OpenAI"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"  
    
    def generate_yoga_flow(self, flow_request: Dict) -> Dict:
        """Generate a yoga flow based on user requirements"""
        
        # Create the prompt
        prompt = self._create_flow_prompt(flow_request)
        print(prompt)
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert yoga instructor with deep knowledge of poses, sequences, and flow creation. Create detailed, safe, and effective yoga flows."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            # Extract the response
            ai_response = response.choices[0].message.content
            
            # Parse the response to extract structured data
            flow_data = self._parse_flow_response(ai_response)
            
            return {
                'success': True,
                'flow_description': flow_data['description'],
                'flow_sequence': flow_data['sequence'],
                'raw_response': ai_response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate yoga flow'
            }
    
    def _create_flow_prompt(self, flow_request: Dict) -> str:
        """Create a detailed prompt for the LLM"""
        
        routine_name = flow_request.get('routineName', 'Custom Flow')
        duration = flow_request.get('timeLength', '30')
        description = flow_request.get('description', '')
        desired_poses = flow_request.get('desiredPoses', '')
        
        prompt = f"""
Create a detailed yoga flow with the following specifications:

**Flow Name:** {routine_name}
**Duration:** {duration} minutes
**User Description:** {description}
**Desired Poses:** {desired_poses if desired_poses else 'No specific poses requested'}

Please provide your response in the following EXACT format:

**FLOW_DESCRIPTION:**
[Provide a detailed description of the flow, including the focus, benefits, and what the practitioner can expect. This should be 2-3 paragraphs.]

**FLOW_SEQUENCE:**
[
  {{"pose": "Pose Name", "duration": 60}},
  {{"pose": "Another Pose", "duration": 45}},
  {{"pose": "Next Pose", "duration": 30}}
]

Guidelines:
- Create a balanced sequence appropriate for the duration
- Include warm-up poses at the beginning
- Progress from easier to more challenging poses
- Include cool-down poses at the end
- Each pose should have a duration in seconds
- Total duration should be approximately {int(duration) * 60} seconds
- Use proper yoga pose names (English or Sanskrit)
- If specific poses are requested, include them in appropriate places
- Consider the user's description for the flow's focus and intensity
"""
        
        return prompt
    
    def _parse_flow_response(self, response: str) -> Dict:
        """Parse the AI response to extract structured data"""
        
        try:
            # Split the response into description and sequence
            parts = response.split('**FLOW_SEQUENCE:**')
            
            description = ""
            sequence = []
            
            if len(parts) >= 2:
                # Extract description
                desc_part = parts[0].replace('**FLOW_DESCRIPTION:**', '').strip()
                description = desc_part
                
                # Extract sequence
                sequence_part = parts[1].strip()
                
                # Try to parse the JSON array
                if sequence_part.startswith('[') and sequence_part.endswith(']'):
                    sequence = json.loads(sequence_part)
                else:
                    # Fallback: try to extract JSON from the text
                    start_idx = sequence_part.find('[')
                    end_idx = sequence_part.rfind(']') + 1
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = sequence_part[start_idx:end_idx]
                        sequence = json.loads(json_str)
            
            return {
                'description': description,
                'sequence': sequence
            }
            
        except Exception as e:
            # Fallback: return the raw response as description
            return {
                'description': response,
                'sequence': []
            }
