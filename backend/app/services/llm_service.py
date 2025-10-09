from openai import OpenAI
import json
import os
import re
import ast
from typing import Dict, List, Tuple

class LLMService:
    """Service for generating yoga flows using OpenAI"""
    
    def __init__(self):
        # Configure a reasonable network timeout to avoid long hangs
        client_timeout = float(os.getenv('OPENAI_TIMEOUT_SECONDS', '30'))
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), timeout=client_timeout)
        self.model = "gpt-3.5-turbo"  
    
    def generate_yoga_flow(self, flow_request: Dict) -> Dict:
        """Generate a yoga flow based on user requirements"""
        
        # Create the initial prompt and constraints
        base_prompt = self._create_flow_prompt(flow_request)
        target_minutes = int(flow_request.get('timeLength', '30') or 30)
        target_seconds = target_minutes * 60
        tolerance_seconds = 300

        try:
            # First attempt
            ai_response = self._call_llm(base_prompt)
            flow_data = self._parse_flow_response(ai_response)

            # Preserve segments if available; otherwise treat all as MAIN
            warm = flow_data.get('warmup', []) if isinstance(flow_data, dict) else []
            main = flow_data.get('main', []) if isinstance(flow_data, dict) else []
            cool = flow_data.get('cooldown', []) if isinstance(flow_data, dict) else []
            if not (warm or main or cool):
                main = flow_data.get('sequence', []) or []

            def combined_total() -> int:
                return self._sum_sequence_duration([*warm, *main, *cool])

            total = combined_total()

            # If too high beyond tolerance, try one more full generation
            if total - target_seconds > tolerance_seconds:
                retry_response = self._call_llm(base_prompt)
                flow_data = self._parse_flow_response(retry_response)
                warm = flow_data.get('warmup', [])
                main = flow_data.get('main', [])
                cool = flow_data.get('cooldown', [])
                if not (warm or main or cool):
                    main = flow_data.get('sequence', []) or []
                total = combined_total()

            # If too low, iteratively top up MAIN routine until within tolerance
            attempts = 0
            max_attempts = 5
            used_pose_names = [s.get('pose') for s in [*warm, *main, *cool] if isinstance(s, dict)]
            while (target_seconds - total) > tolerance_seconds and attempts < max_attempts:
                deficit = max(0, target_seconds - total)
                topup_prompt = self._create_topup_prompt(flow_request, deficit, used_pose_names)
                topup_response = self._call_llm(topup_prompt)
                additions = self._parse_sequence_array(topup_response)
                # Insert additions into MAIN before cooldown
                for item in additions:
                    if isinstance(item, dict) and item.get('pose'):
                        normalized = {
                            'pose': item.get('pose'),
                            'duration': int(float(item.get('duration', 0))) if str(item.get('duration', '')).strip() != '' else 0,
                            'description': item.get('description') or ''
                        }
                        main.append(normalized)
                        used_pose_names.append(normalized['pose'])
                total = combined_total()
                attempts += 1

            final_sequence = [*warm, *main, *cool]
            if final_sequence and abs(total - target_seconds) <= tolerance_seconds:
                return {
                    'success': True,
                    'flow_description': flow_data.get('description', ''),
                    'flow_sequence': final_sequence,
                    'raw_response': ai_response
                }

            return {
                'success': False,
                'message': 'Unable to produce flow within time tolerance',
                'error': f'total_seconds={total}, target_seconds={target_seconds}'
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
**Duration:** {duration} minutes - IT IS VERY IMPORTANT TO FOLLOW THE DURATION OF THE FLOW. DO NOT RETURN A FLOW WHERE THE SUM OF THE TIMES IS SIGNIFICANTLY DIFFERENT THAN THE DURATION.
**User Description:** {description}
**Desired Poses:** {desired_poses if desired_poses else 'No specific poses requested'}

Please provide your response in the following EXACT format:

**FLOW_DESCRIPTION:**
[Provide a detailed description of the flow, including the focus, benefits, and what the practitioner can expect. This should be 1-2 short paragraphs.]

**WARMUP_SEQUENCE:**
[
  {{"pose": "Pose Name", "duration": 60, "description": "Concrete body setup and entry cues."}}
]

**MAIN_SEQUENCE:**
[
  {{"pose": "Pose Name", "duration": 45, "description": "Concrete alignment and key actions."}}
]

**COOLDOWN_SEQUENCE:**
[
  {{"pose": "Pose Name", "duration": 60, "description": "Gentle alignment and release cues."}}
]

Guidelines:
- Create a balanced sequence appropriate for the duration. - IT IS VERY IMPORTANT TO FOLLOW THE DURATION OF THE FLOW. DO NOT RETURN A FLOW WHERE THE SUM OF THE TIMES IS SIGNIFICANTLY DIFFERENT THAN THE DURATION.
- Include warm-up poses at the beginning
- Progress from easier to more challenging poses in MAIN
- Include cool-down poses at the end
- Each pose should have a duration in seconds
- Each pose MUST include 1–3 short, concrete alignment sentences giving exact body orientation and key actions (joint stacking, limb positions, spinal shape, weight distribution, engagement, and gaze)
- Use clear imperative cues (e.g., "stack", "press", "draw") and avoid vague wording like "feel", "focus", or generic benefits
- Prioritize setup/entry and alignment; do not include philosophy or long benefits in the pose descriptions
- There are no limits on how many poses you can include in the flow. Please to not limit yourself. It is preffered that the flow has more poses rather than few poses for longer durations.
- Again, please bias your flow generation towards having flows that meet the duration and have more poses for shorter durations rather than fewer poses for longer durations.
- Total duration should be approximately {int(duration) * 60} seconds - IT IS VERY IMPORTANT TO FOLLOW THE DURATION OF THE FLOW. DO NOT RETURN A FLOW WHERE THE SUM OF THE TIMES IS SIGNIFICANTLY DIFFERENT THAN THE DURATION.
- Use proper yoga pose names (English or Sanskrit)
- If specific poses are requested, include them in appropriate places
- Consider the user's description for the flow's focus and intensity
"""
        
        return prompt

    def _call_llm(self, prompt: str) -> str:
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
            max_tokens=1200,
            temperature=0.7
        )
        return response.choices[0].message.content

    def _create_topup_prompt(self, flow_request: Dict, deficit_seconds: int, used_pose_names: List[str]) -> str:
        routine_name = flow_request.get('routineName', 'Custom Flow')
        description = flow_request.get('description', '')
        desired_poses = flow_request.get('desiredPoses', '')

        used_list = ', '.join([p for p in used_pose_names if p]) or 'None'
        return f"""
We need to extend ONLY the MAIN routine of the existing flow.
Add additional poses whose total duration is as close as possible to {deficit_seconds} seconds (do not exceed by more than 300 seconds). Prefer batches totalling 120–240 seconds to reduce response size; you may be called repeatedly.

Avoid repeating too many poses. Poses already used: {used_list}

Respond with ONLY a JSON array (no prose, no code fences) where each item is:
{{"pose": "Pose Name", "duration": 30, "description": "Concrete alignment/entry cues."}}
"""

    def _parse_sequence_array(self, text: str) -> List[Dict]:
        """Extract the first JSON-like array of dicts from arbitrary text."""
        # Remove code fences
        cleaned = re.sub(r"```(?:json)?|```", "", text, flags=re.IGNORECASE)
        m = re.search(r"\[\s*\{[\s\S]*?\}\s*\]", cleaned)
        array_text = m.group(0) if m else ''
        if not array_text:
            start = cleaned.find('[')
            end = cleaned.rfind(']') + 1
            if start != -1 and end > start:
                array_text = cleaned[start:end]
        if not array_text:
            return []
        array_text = re.sub(r",\s*([}\]])", r"\1", array_text)
        try:
            return json.loads(array_text)
        except Exception:
            try:
                return ast.literal_eval(array_text)
            except Exception:
                return []

    def _sum_sequence_duration(self, sequence: List[Dict]) -> int:
        total = 0
        for item in sequence:
            try:
                total += int(float(item.get('duration', 0)))
            except Exception:
                continue
        return total
    
    def _parse_flow_response(self, response: str) -> Dict:
        """Parse the AI response to extract structured data.

        Supports both the legacy single **FLOW_SEQUENCE:** array format and the
        new split format: **WARMUP_SEQUENCE:**, **MAIN_SEQUENCE:**, **COOLDOWN_SEQUENCE:**.
        Returns a combined 'sequence' list.
        """
        
        try:
            # First, extract description
            description = re.split(r"\*\*FLOW_DESCRIPTION:\*\*", response)
            if len(description) > 1:
                # everything after marker until next marker
                after_desc = description[1]
            else:
                after_desc = response

            # Try split-format sequences
            warm_text = re.split(r"\*\*WARMUP_SEQUENCE:\*\*", response)
            main_text = re.split(r"\*\*MAIN_SEQUENCE:\*\*", response)
            cool_text = re.split(r"\*\*COOLDOWN_SEQUENCE:\*\*", response)

            description_text = response
            if len(description) > 1:
                description_text = description[1].split('**WARMUP_SEQUENCE:**')[0].split('**FLOW_SEQUENCE:**')[0].strip()

            def extract_first_array(block: str) -> str:
                block = re.sub(r"```(?:json)?|```", "", block, flags=re.IGNORECASE)
                m = re.search(r"\[\s*\{[\s\S]*?\}\s*\]", block)
                if m:
                    return m.group(0)
                start_idx = block.find('[')
                end_idx = block.rfind(']') + 1
                return block[start_idx:end_idx] if start_idx != -1 and end_idx > start_idx else ''

            def load_array(arr_text: str) -> List[Dict]:
                if not arr_text:
                    return []
                cleaned = re.sub(r",\s*([}\]])", r"\1", arr_text)
                try:
                    return json.loads(cleaned)
                except Exception:
                    try:
                        return ast.literal_eval(cleaned)
                    except Exception:
                        return []
            
            # Attempt split sequences first
            warm_seq: List[Dict] = []
            main_seq: List[Dict] = []
            cool_seq: List[Dict] = []

            if len(warm_text) > 1:
                warm_seq = load_array(extract_first_array(warm_text[1]))
            if len(main_text) > 1:
                main_seq = load_array(extract_first_array(main_text[1]))
            if len(cool_text) > 1:
                cool_seq = load_array(extract_first_array(cool_text[1]))

            sequence_raw: List[Dict]
            if warm_seq or main_seq or cool_seq:
                sequence_raw = [*warm_seq, *main_seq, *cool_seq]
            else:
                # Fallback: legacy **FLOW_SEQUENCE:** format
                parts = response.split('**FLOW_SEQUENCE:**')
                sequence_part = parts[1].strip() if len(parts) >= 2 else ''
                sequence_raw = load_array(extract_first_array(sequence_part))

            # Normalize items
            normalized: List[Dict] = []
            for item in sequence_raw or []:
                if not isinstance(item, dict):
                    continue
                pose = item.get('pose') or item.get('name') or ''
                raw_dur = item.get('duration', 0)
                try:
                    duration = int(float(raw_dur))
                except Exception:
                    duration = 0
                pose_desc = item.get('description') or item.get('cue') or item.get('cues') or ''
                normalized.append({
                    'pose': pose,
                    'duration': duration,
                    'description': pose_desc,
                })

            # Description clean
            description = description_text.replace('**', '').strip()
            sequence = normalized

            # Also return split segments if present to allow precise insertion
            result: Dict = {
                'description': description,
                'sequence': sequence
            }
            if warm_seq or main_seq or cool_seq:
                # Provide normalized split lists
                def norm(seq: List[Dict]) -> List[Dict]:
                    out: List[Dict] = []
                    for item in seq or []:
                        if not isinstance(item, dict):
                            continue
                        pose = item.get('pose') or item.get('name') or ''
                        try:
                            duration = int(float(item.get('duration', 0)))
                        except Exception:
                            duration = 0
                        out.append({
                            'pose': pose,
                            'duration': duration,
                            'description': item.get('description') or ''
                        })
                    return out
                result['warmup'] = norm(warm_seq)
                result['main'] = norm(main_seq)
                result['cooldown'] = norm(cool_seq)
            
            return result
            
        except Exception as e:
            # Fallback: return the raw response as description
            return {
                'description': response,
                'sequence': []
            }
