# Prompt Enhancer Tests

This folder contains tests for the prompt_enhancer module.

## Structure

```
tests/
├── __init__.py
├── README.md
├── run_tests.py
└── pipeline_tests/
    ├── __init__.py
    └── test_examples.py
```

## Running Tests

### Run all tests:

```bash
python -m prompt_enhancer.tests.run_tests
```

### Run pipeline tests only:

```bash
python prompt_enhancer/tests/pipeline_tests/test_examples.py
```

## Test Cases

### Pipeline Tests

The pipeline tests verify that the correction pipeline works correctly:

1. **Input → Corrected**: Fixes typos and sentence structure
2. **Corrected → LLM-Friendly**: Makes text more explicit for language models
3. **Final Result**: The output after both stages

### Example Test Cases

1. **Basic conversation with friends**

   - Input: "საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბირეთ."
   - Expected: Adds "ჩვენ" for clarity

2. **Hackathon participation**

   - Input: "დრეს ვმონაწილეობდი ჰაკათონში და მაგარ დროს ვატარებდი."
   - Expected: Fixes "დრეს" to "დღეს" and adds "მე"

3. **School visit**

   - Input: "სკოლაში წავედი და მასწავლებელს შევხვდი."
   - Expected: Adds "მე" for clarity

4. **Friend's job change**
   - Input: "ჩემი მეგობარი თბილისში წავიდა და ახალი სამსახური დაიწყო."
   - Expected: No changes needed (subject already clear)

## Adding New Tests

To add new test cases:

1. Add the test case to `pipeline_tests/test_examples.py`
2. Include input, expected corrected, expected LLM-friendly, and expected final outputs
3. Run the tests to verify they pass

## Test Output

Tests will show:

- ✅ PASS: All stages match expected output
- ❌ FAIL: One or more stages don't match expected output
