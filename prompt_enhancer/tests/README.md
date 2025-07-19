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
    ├── test_examples.py
    └── test_structure.py
```

## Running Tests

### Run all tests:

```bash
python -m prompt_enhancer.tests.run_tests
```

### Run specific test types:

```bash
# Run only pipeline tests
python -m prompt_enhancer.tests.run_tests --pipeline

# Run only structure tests
python -m prompt_enhancer.tests.run_tests --structure

# Show help
python -m prompt_enhancer.tests.run_tests --help
```

### Run specific test numbers:

```bash
# Run specific tests
python -m prompt_enhancer.tests.run_tests --pipeline 1,2,3

# Run range of tests
python -m prompt_enhancer.tests.run_tests --pipeline 4-8

# Run specific tests (non-sequential)
python -m prompt_enhancer.tests.run_tests --pipeline 3,5,6,7
```

### Run pipeline tests directly:

```bash
# Run all pipeline tests
python prompt_enhancer/tests/pipeline_tests/test_examples.py

# Run specific tests
python prompt_enhancer/tests/pipeline_tests/test_examples.py "1,2,3"
python prompt_enhancer/tests/pipeline_tests/test_examples.py "4-8"
```

## Test Cases

### Pipeline Tests (10 total)

The pipeline tests verify that the correction pipeline works correctly:

1. **Input → Corrected**: Fixes typos and sentence structure
2. **Corrected → LLM-Friendly**: Makes text more explicit for language models
3. **Final Result**: The output after both stages

### Test Case Details

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

5. **Someone went to school and sang**

   - Input: "სკოლაში წავიდა და მეგობრებთან ერთად იმღერა."
   - Expected: Adds "ის" for clarity

6. **Children made a project**

   - Input: "ბავშვებმა სკოლაში ახალი პროექტი გააკეთეს."
   - Expected: No changes needed (subject already clear)

7. **Evening was good, talked with friends (multiple typos)**

   - Input: "საღამო კბარი იყო, მობეგრებთან ერთად ვისაუბერით."
   - Expected: Fixes multiple typos and adds "ჩვენ"

8. **School visit with typos**

   - Input: "სკოლაშ წავეი და მასწავლეელს შევხვდი."
   - Expected: Fixes typos and adds "მე"

9. **Today I went to school and saw teacher**

   - Input: "დეს მე მივედი სკოლაში და მასწავლებელ ვნახე."
   - Expected: Fixes typos and reorders "მე"

10. **Today we went and spent evening together**
    - Input: "დრეს წასვლა და საღამო ერთად გავატარეთ."
    - Expected: Fixes typos and adds "ჩვენ"

## Adding New Tests

To add new test cases:

1. Add the test case to `pipeline_tests/test_examples.py`
2. Include input, expected corrected, expected LLM-friendly, and expected final outputs
3. Run the tests to verify they pass

## Test Output

Tests will show:

- ✅ PASS: All stages match expected output
- ❌ FAIL: One or more stages don't match expected output

## Test Number Format

- **Single numbers**: `1`, `2`, `3`
- **Ranges**: `4-8` (includes both 4 and 8)
- **Mixed**: `1,3,5-7,9` (combines single numbers and ranges)
- **All tests**: No specification (runs all 10 tests)
