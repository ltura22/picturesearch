"""
Pipeline Test Examples
These are expected outputs for the pipeline correction process
"""

# Test case 1: Basic conversation with friends
TEST_CASE_1 = {
    "input": "საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბირეთ.",
    "expected_corrected": "საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბრეთ.",
    "expected_llm_friendly": "საღამო კარგი იყო, ჩვენ მეგობრებთან ერთად ვისაუბრეთ.",
    "expected_final": "საღამო კარგი იყო, ჩვენ მეგობრებთან ერთად ვისაუბრეთ.",
    "description": "Basic conversation with friends - adds 'ჩვენ' for clarity"
}

# Test case 2: Hackathon participation
TEST_CASE_2 = {
    "input": "დრეს ვმონაწილეობდი ჰაკათონში და მაგარ დროს ვატარებდი.",
    "expected_corrected": "დღეს ვმონაწილეობდი ჰაკათონში და მაგარ დროს ვატარებდი.",
    "expected_llm_friendly": "მე დღეს ვმონაწილეობდი ჰაკათონში და მაგარ დროს ვატარებდი.",
    "expected_final": "მე დღეს ვმონაწილეობდი ჰაკათონში და მაგარ დროს ვატარებდი.",
    "description": "Hackathon participation - fixes 'დრეს' to 'დღეს' and adds 'მე'"
}

# Test case 3: School visit
TEST_CASE_3 = {
    "input": "სკოლაში წავედი და მასწავლებელს შევხვდი.",
    "expected_corrected": "სკოლაში წავედი და მასწავლებელს შევხვდი.",
    "expected_llm_friendly": "მე სკოლაში წავედი და მასწავლებელს შევხვდი.",
    "expected_final": "მე სკოლაში წავედი და მასწავლებელს შევხვდი.",
    "description": "School visit - adds 'მე' for clarity"
}

# Test case 4: Friend's job change
TEST_CASE_4 = {
    "input": "ჩემი მეგობარი თბილისში წავიდა და ახალი სამსახური დაიწყო.",
    "expected_corrected": "ჩემი მეგობარი თბილისში წავიდა და ახალი სამსახური დაიწყო.",
    "expected_llm_friendly": "ჩემი მეგობარი თბილისში წავიდა და ახალი სამსახური დაიწყო.",
    "expected_final": "ჩემი მეგობარი თბილისში წავიდა და ახალი სამსახური დაიწყო.",
    "description": "Friend's job change - no changes needed as subject is already clear"
}

# All test cases
PIPELINE_TEST_CASES = [
    TEST_CASE_1,
    TEST_CASE_2,
    TEST_CASE_3,
    TEST_CASE_4
]

def run_pipeline_tests():
    """Run all pipeline test cases"""
    from prompt_enhancer.georgian_corrector import pipeline_correct_georgian
    
    print("Pipeline Test Suite")
    print("=" * 60)
    
    for i, test_case in enumerate(PIPELINE_TEST_CASES, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print("-" * 40)
        
        # Run the pipeline
        result = pipeline_correct_georgian(test_case['input'], show_steps=False)
        
        # Check results
        print(f"Input: {test_case['input']}")
        print(f"Expected Corrected: {test_case['expected_corrected']}")
        print(f"Actual Corrected: {result['corrected']}")
        print(f"Expected LLM-Friendly: {test_case['expected_llm_friendly']}")
        print(f"Actual LLM-Friendly: {result['llm_friendly']}")
        print(f"Expected Final: {test_case['expected_final']}")
        print(f"Actual Final: {result['final']}")
        
        # Check if results match expectations
        corrected_match = result['corrected'] == test_case['expected_corrected']
        llm_friendly_match = result['llm_friendly'] == test_case['expected_llm_friendly']
        final_match = result['final'] == test_case['expected_final']
        
        if corrected_match and llm_friendly_match and final_match:
            print("✅ PASS")
        else:
            print("❌ FAIL")
            if not corrected_match:
                print(f"  - Corrected stage mismatch")
            if not llm_friendly_match:
                print(f"  - LLM-friendly stage mismatch")
            if not final_match:
                print(f"  - Final result mismatch")

if __name__ == "__main__":
    run_pipeline_tests() 