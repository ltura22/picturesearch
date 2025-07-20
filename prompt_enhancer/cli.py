"""
Command Line Interface for Georgian Text Correction
"""

import argparse
import sys
import json
from .georgian_corrector import GeorgianTextCorrector, correct_georgian_text
from .api import GeorgianCorrectionAPI

def main():
    parser = argparse.ArgumentParser(description="Georgian Text Correction Tool")
    parser.add_argument("text", nargs="?", help="Text to correct")
    parser.add_argument("--style", "-s", default="auto", 
                       choices=["basic", "advanced", "contextual", "formal", "casual", "corrected", "llm_friendly", "translate_to_english", "simplify", "auto"],
                       help="Correction style")
    parser.add_argument("--file", "-f", help="Input file with text to correct")
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument("--batch", "-b", action="store_true", help="Process multiple lines")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    parser.add_argument("--stats", action="store_true", help="Show correction statistics")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--pipeline", "-p", action="store_true", help="Run pipeline: corrected -> llm_friendly")
    parser.add_argument("--translate", "-t", action="store_true", help="Include translation in pipeline")
    parser.add_argument("--simplify-pipeline", action="store_true", help="Run simplify pipeline: corrected -> simplified")
    parser.add_argument("--agent", action="store_true", help="Use photo agent (auto-detects photo search and applies simplify pipeline)")
    
    args = parser.parse_args()
    
    api = GeorgianCorrectionAPI()
    
    if args.interactive:
        interactive_mode(api)
    elif args.pipeline:
        if args.text:
            process_pipeline_text(args.text, args.json, args.stats, api, args.translate)
        elif args.file:
            process_pipeline_file(args.file, args.output, args.batch, args.json, args.stats, api, args.translate)
        else:
            print("No text provided for pipeline. Use --help for usage information.")
            sys.exit(1)
    elif args.simplify_pipeline:
        if args.text:
            process_simplify_pipeline_text(args.text, args.json, args.stats, api)
        elif args.file:
            process_simplify_pipeline_file(args.file, args.output, args.batch, args.json, args.stats, api)
        else:
            print("No text provided for simplify pipeline. Use --help for usage information.")
            sys.exit(1)
    elif args.agent:
        if args.text:
            process_agent_text(args.text, args.json, args.stats, api)
        elif args.file:
            process_agent_file(args.file, args.output, args.batch, args.json, args.stats, api)
        else:
            print("No text provided for agent. Use --help for usage information.")
            sys.exit(1)
    elif args.file:
        process_file(args.file, args.output, args.style, args.batch, args.json, args.stats, api)
    elif args.text:
        process_single_text(args.text, args.style, args.json, args.stats, api)
    else:
        print("No text provided. Use --help for usage information.")
        sys.exit(1)

def interactive_mode(api):
    """Interactive mode for text correction"""
    print("Georgian Text Correction - Interactive Mode")
    print("Type 'quit' to exit, 'help' for commands")
    print("=" * 50)
    
    while True:
        try:
            text = input("\nEnter Georgian text to correct: ").strip()
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif text.lower() == 'help':
                print_help()
                continue
            elif text.lower() == 'styles':
                styles = api.get_available_styles()
                print(f"Available styles: {', '.join(styles)}")
                continue
            elif not text:
                continue
            
            style = input("Style (auto/basic/advanced/formal/casual/corrected/llm_friendly): ").strip() or "auto"
            
            result = api.correct_single(text, style)
            
            if result.get("success"):
                print(f"\nOriginal: {result['original']}")
                print(f"Corrected: {result['corrected']}")
                if result.get('stats'):
                    stats = result['stats']
                    print(f"Changes: {stats['character_changes']} characters, {stats['words_changed']} words")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def process_single_text(text, style, json_output, show_stats, api):
    """Process a single text input"""
    result = api.correct_single(text, style)
    
    if json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("success"):
            print(f"Original: {result['original']}")
            print(f"Corrected: {result['corrected']}")
            if show_stats and result.get('stats'):
                stats = result['stats']
                print(f"Statistics: {stats}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")

def process_file(input_file, output_file, style, batch, json_output, show_stats, api):
    """Process text from a file"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            if batch:
                texts = [line.strip() for line in f if line.strip()]
                result = api.correct_batch(texts, style)
            else:
                text = f.read().strip()
                result = api.correct_single(text, style)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                if json_output:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                else:
                    if result.get("success"):
                        if batch:
                            for i, res in enumerate(result['results']):
                                f.write(f"Text {i+1}:\n")
                                f.write(f"Original: {res['original']}\n")
                                f.write(f"Corrected: {res['corrected']}\n")
                                if show_stats:
                                    f.write(f"Stats: {res['stats']}\n")
                                f.write("\n")
                        else:
                            f.write(f"Original: {result['original']}\n")
                            f.write(f"Corrected: {result['corrected']}\n")
                            if show_stats:
                                f.write(f"Stats: {result['stats']}\n")
                    else:
                        f.write(f"Error: {result.get('error', 'Unknown error')}")
        else:
            if json_output:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                if result.get("success"):
                    if batch:
                        for i, res in enumerate(result['results']):
                            print(f"Text {i+1}:")
                            print(f"Original: {res['original']}")
                            print(f"Corrected: {res['corrected']}")
                            if show_stats:
                                print(f"Stats: {res['stats']}")
                            print()
                    else:
                        print(f"Original: {result['original']}")
                        print(f"Corrected: {result['corrected']}")
                        if show_stats:
                            print(f"Stats: {result['stats']}")
                else:
                    print(f"Error: {result.get('error', 'Unknown error')}")
                    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def process_pipeline_text(text, json_output, show_stats, api, translate):
    """Process a single text through the pipeline"""
    from .georgian_corrector import pipeline_correct_georgian
    
    result = pipeline_correct_georgian(text, show_steps=True, include_translation=translate)
    
    if json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if "error" not in result:
            if show_stats:
                # Calculate stats for the pipeline
                input_len = len(result["input"])
                final_len = len(result["final"])
                changes = sum(1 for a, b in zip(result["input"], result["final"]) if a != b)
                print(f"\nPipeline Statistics:")
                print(f"  Input length: {input_len}")
                print(f"  Final length: {final_len}")
                print(f"  Character changes: {changes}")
                print(f"  Improvement ratio: {final_len/input_len:.2f}")

def process_pipeline_file(input_file, output_file, batch, json_output, show_stats, api, translate):
    """Process text from a file through the pipeline"""
    from .georgian_corrector import batch_pipeline_correct_georgian
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            if batch:
                texts = [line.strip() for line in f if line.strip()]
                results = batch_pipeline_correct_georgian(texts, show_steps=True, include_translation=translate)
            else:
                text = f.read().strip()
                results = [pipeline_correct_georgian(text, show_steps=True, include_translation=translate)]
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                if json_output:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                else:
                    for i, result in enumerate(results, 1):
                        f.write(f"Text {i} Pipeline Results:\n")
                        f.write(f"Input: {result['input']}\n")
                        f.write(f"Corrected: {result['corrected']}\n")
                        f.write(f"LLM-Friendly: {result['llm_friendly']}\n")
                        f.write(f"Final: {result['final']}\n")
                        if show_stats:
                            input_len = len(result["input"])
                            final_len = len(result["final"])
                            changes = sum(1 for a, b in zip(result["input"], result["final"]) if a != b)
                            f.write(f"Stats: {changes} changes, ratio: {final_len/input_len:.2f}\n")
                        f.write("\n")
        else:
            if json_output:
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                for i, result in enumerate(results, 1):
                    print(f"\nText {i} Final Result: {result['final']}")
                    if show_stats:
                        input_len = len(result["input"])
                        final_len = len(result["final"])
                        changes = sum(1 for a, b in zip(result["input"], result["final"]) if a != b)
                        print(f"Stats: {changes} changes, ratio: {final_len/input_len:.2f}")
                    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def process_simplify_pipeline_text(text, json_output, show_stats, api):
    """Process a single text through the simplify pipeline"""
    from .georgian_corrector import simplify_pipeline_correct_georgian
    
    result = simplify_pipeline_correct_georgian(text, show_steps=True)
    
    if json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if "error" not in result:
            if show_stats:
                # Calculate stats for the simplify pipeline
                input_len = len(result["input"])
                final_len = len(result["final"])
                changes = sum(1 for a, b in zip(result["input"], result["final"]) if a != b)
                print(f"\nSimplify Pipeline Statistics:")
                print(f"  Input length: {input_len}")
                print(f"  Final length: {final_len}")
                print(f"  Character changes: {changes}")
                print(f"  Simplification ratio: {final_len/input_len:.2f}")

def process_simplify_pipeline_file(input_file, output_file, batch, json_output, show_stats, api):
    """Process text from a file through the simplify pipeline"""
    from .georgian_corrector import batch_simplify_pipeline_correct_georgian, simplify_pipeline_correct_georgian
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            if batch:
                texts = [line.strip() for line in f if line.strip()]
                results = batch_simplify_pipeline_correct_georgian(texts, show_steps=True)
            else:
                text = f.read().strip()
                results = [simplify_pipeline_correct_georgian(text, show_steps=True)]
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                if json_output:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                else:
                    for i, result in enumerate(results, 1):
                        f.write(f"Query {i} Simplify Pipeline Results:\n")
                        f.write(f"Input: {result['input']}\n")
                        f.write(f"Corrected: {result['corrected']}\n")
                        f.write(f"Simplified: {result['simplified']}\n")
                        f.write(f"Final: {result['final']}\n")
                        if show_stats:
                            input_len = len(result["input"])
                            final_len = len(result["final"])
                            changes = sum(1 for a, b in zip(result["input"], result["final"]) if a != b)
                            f.write(f"Stats: {changes} changes, ratio: {final_len/input_len:.2f}\n")
                        f.write("\n")
        else:
            if json_output:
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                for i, result in enumerate(results, 1):
                    print(f"\nQuery {i} Final Result: {result['final']}")
                    if show_stats:
                        input_len = len(result["input"])
                        final_len = len(result["final"])
                        changes = sum(1 for a, b in zip(result["input"], result["final"]) if a != b)
                        print(f"Stats: {changes} changes, ratio: {final_len/input_len:.2f}")
                    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def process_agent_text(text, json_output, show_stats, api):
    """Process a single text through the photo agent"""
    from .georgian_corrector import process_photo_prompt
    
    result = process_photo_prompt(text, show_steps=True)
    
    if json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\nPhoto Agent Results:")
        print(f"  Original: {result['original']}")
        print(f"  Is Photo Search: {result['is_photo_search']}")
        print(f"  Photo Count: {result['photo_count']}")
        print(f"  Simplified Query: {result['simplified_query']}")
        print(f"  Processing Type: {result['processing_type']}")
        
        if show_stats and result.get('pipeline_steps'):
            pipeline = result['pipeline_steps']
            input_len = len(pipeline["input"])
            final_len = len(pipeline["final"])
            changes = sum(1 for a, b in zip(pipeline["input"], pipeline["final"]) if a != b)
            print(f"\nAgent Statistics:")
            print(f"  Input length: {input_len}")
            print(f"  Final length: {final_len}")
            print(f"  Character changes: {changes}")
            print(f"  Simplification ratio: {final_len/input_len:.2f}")

def process_agent_file(input_file, output_file, batch, json_output, show_stats, api):
    """Process text from a file through the photo agent"""
    from .georgian_corrector import batch_process_photo_prompts, process_photo_prompt
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            if batch:
                texts = [line.strip() for line in f if line.strip()]
                results = batch_process_photo_prompts(texts, show_steps=True)
            else:
                text = f.read().strip()
                results = [process_photo_prompt(text, show_steps=True)]
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                if json_output:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                else:
                    for i, result in enumerate(results, 1):
                        f.write(f"Prompt {i} Agent Results:\n")
                        f.write(f"Original: {result['original']}\n")
                        f.write(f"Is Photo Search: {result['is_photo_search']}\n")
                        f.write(f"Photo Count: {result['photo_count']}\n")
                        f.write(f"Simplified Query: {result['simplified_query']}\n")
                        f.write(f"Processing Type: {result['processing_type']}\n")
                        if show_stats and result.get('pipeline_steps'):
                            pipeline = result['pipeline_steps']
                            input_len = len(pipeline["input"])
                            final_len = len(pipeline["final"])
                            changes = sum(1 for a, b in zip(pipeline["input"], pipeline["final"]) if a != b)
                            f.write(f"Stats: {changes} changes, ratio: {final_len/input_len:.2f}\n")
                        f.write("\n")
        else:
            if json_output:
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                for i, result in enumerate(results, 1):
                    print(f"\nPrompt {i} Results:")
                    print(f"  Original: {result['original']}")
                    print(f"  Is Photo Search: {result['is_photo_search']}")
                    print(f"  Photo Count: {result['photo_count']}")
                    print(f"  Final Query: {result['simplified_query']}")
                    if show_stats and result.get('pipeline_steps'):
                        pipeline = result['pipeline_steps']
                        input_len = len(pipeline["input"])
                        final_len = len(pipeline["final"])
                        changes = sum(1 for a, b in zip(pipeline["input"], pipeline["final"]) if a != b)
                        print(f"  Stats: {changes} changes, ratio: {final_len/input_len:.2f}")
                    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def print_help():
    """Print help information"""
    print("\nCommands:")
    print("  help    - Show this help")
    print("  styles  - Show available correction styles")
    print("  quit    - Exit the program")
    print("\nStyles:")
    print("  auto         - Auto-detect style (default)")
    print("  basic        - Basic correction")
    print("  advanced     - Advanced correction with context")
    print("  formal       - Formal/business style")
    print("  casual       - Casual/informal style")
    print("  corrected    - Only fix typos and sentence structure")
    print("  llm_friendly - Make text more LLM-friendly with explicit references")
    print("  translate_to_english - Translate Georgian text to English")
    print("\nPipeline:")
    print("  Use --pipeline to run: Input -> Corrected -> LLM-Friendly -> Output")
    print("  Use --translate with --pipeline to include translation.")
    print("  Use --simplify-pipeline to run: Input -> Corrected -> Simplified -> Output")
    print("  Use --agent for automatic photo search detection and processing")

if __name__ == "__main__":
    main() 