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

# Test case 5: Someone went to school and sang
TEST_CASE_5 = {
    "input": "სკოლაში წავიდა და მეგობრებთან ერთად იმღერა.",
    "expected_corrected": "სკოლაში წავიდა და მეგობრებთან ერთად იმღერა.",
    "expected_llm_friendly": "ის სკოლაში წავიდა და მეგობრებთან ერთად იმღერა.",
    "expected_final": "ის სკოლაში წავიდა და მეგობრებთან ერთად იმღერა.",
    "description": "Someone went to school and sang - adds 'ის' for clarity"
}

# Test case 6: Children made a project
TEST_CASE_6 = {
    "input": "ბავშვებმა სკოლაში ახალი პროექტი გააკეთეს.",
    "expected_corrected": "ბავშვებმა სკოლაში ახალი პროექტი გააკეთეს.",
    "expected_llm_friendly": "ბავშვებმა სკოლაში ახალი პროექტი გააკეთეს.",
    "expected_final": "ბავშვებმა სკოლაში ახალი პროექტი გააკეთეს.",
    "description": "Children made a project - no changes needed as subject is clear"
}

# Test case 7: Evening was good, talked with friends (multiple typos)
TEST_CASE_7 = {
    "input": "საღამო კბარი იყო, მობეგრებთან ერთად ვისაუბერით.",
    "expected_corrected": "საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბრეთ.",
    "expected_llm_friendly": "საღამო კარგი იყო, ჩვენ მეგობრებთან ერთად ვისაუბრეთ.",
    "expected_final": "საღამო კარგი იყო, ჩვენ მეგობრებთან ერთად ვისაუბრეთ.",
    "description": "Evening was good, talked with friends - fixes multiple typos and adds 'ჩვენ'"
}

# Test case 8: School visit with typos
TEST_CASE_8 = {
    "input": "სკოლაშ წავეი და მასწავლეელს შევხვდი.",
    "expected_corrected": "სკოლაში წავედი და მასწავლებელს შევხვდი.",
    "expected_llm_friendly": "მე სკოლაში წავედი და მასწავლებელს შევხვდი.",
    "expected_final": "მე სკოლაში წავედი და მასწავლებელს შევხვდი.",
    "description": "School visit with typos - fixes typos and adds 'მე'"
}

# Test case 9: Today I went to school and saw teacher
TEST_CASE_9 = {
    "input": "დეს მე მივედი სკოლაში და მასწავლებელ ვნახე.",
    "expected_corrected": "დღეს მე სკოლაში მივედი და მასწავლებელი ვნახე.",
    "expected_llm_friendly": "მე დღეს სკოლაში მივედი და მასწავლებელი ვნახე.",
    "expected_final": "მე დღეს სკოლაში მივედი და მასწავლებელი ვნახე.",
    "description": "Today I went to school and saw teacher - fixes typos and reorders 'მე'"
}

# Test case 10: Today we went and spent evening together
TEST_CASE_10 = {
    "input": "დრეს წასვლა და საღამო ერთად გავატარეთ.",
    "expected_corrected": "დღეს წავედით და საღამო ერთად გავატარეთ.",
    "expected_llm_friendly": "ჩვენ დღეს წავედით და საღამო ერთად გავატარეთ.",
    "expected_final": "ჩვენ დღეს წავედით და საღამო ერთად გავატარეთ.",
    "description": "Today we went and spent evening together - fixes typos and adds 'ჩვენ'"
}

# All test cases
PIPELINE_TEST_CASES = [
    TEST_CASE_1,
    TEST_CASE_2,
    TEST_CASE_3,
    TEST_CASE_4,
    TEST_CASE_5,
    TEST_CASE_6,
    TEST_CASE_7,
    TEST_CASE_8,
    TEST_CASE_9,
    TEST_CASE_10
]

def run_pipeline_tests(test_numbers=None):
    """Run pipeline test cases
    
    Args:
        test_numbers: List of test numbers to run (1-based), or None for all tests
                     Can be specified as: [1,2,3] or range like [4,5,6,7,8]
    """
    from prompt_enhancer.georgian_corrector import pipeline_correct_georgian
    
    print("Pipeline Test Suite")
    print("=" * 60)
    
    # Determine which tests to run
    if test_numbers is None:
        tests_to_run = range(len(PIPELINE_TEST_CASES))
    else:
        # Convert 1-based numbers to 0-based indices
        tests_to_run = [num - 1 for num in test_numbers if 1 <= num <= len(PIPELINE_TEST_CASES)]
    
    if not tests_to_run:
        print("No valid test numbers provided.")
        return
    
    for i in tests_to_run:
        test_case = PIPELINE_TEST_CASES[i]
        test_number = i + 1
        
        print(f"\nTest Case {test_number}: {test_case['description']}")
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

def parse_test_numbers(test_spec):
    """Parse test number specification like '4-8' or '3,5,6,7'"""
    if not test_spec:
        return None
    
    test_numbers = []
    parts = test_spec.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Range like '4-8'
            try:
                start, end = map(int, part.split('-'))
                test_numbers.extend(range(start, end + 1))
            except ValueError:
                print(f"Invalid range format: {part}")
        else:
            # Single number
            try:
                test_numbers.append(int(part))
            except ValueError:
                print(f"Invalid number: {part}")
    
    return sorted(list(set(test_numbers)))  # Remove duplicates and sort

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_spec = sys.argv[1]
        test_numbers = parse_test_numbers(test_spec)
        if test_numbers:
            print(f"Running tests: {test_numbers}")
            run_pipeline_tests(test_numbers)
        else:
            print("Invalid test specification. Use format like '1,2,3' or '4-8'")
    else:
        run_pipeline_tests() 