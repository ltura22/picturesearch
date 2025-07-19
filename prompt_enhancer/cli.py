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
                       choices=["basic", "advanced", "contextual", "formal", "casual", "corrected", "auto"],
                       help="Correction style")
    parser.add_argument("--file", "-f", help="Input file with text to correct")
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument("--batch", "-b", action="store_true", help="Process multiple lines")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    parser.add_argument("--stats", action="store_true", help="Show correction statistics")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    api = GeorgianCorrectionAPI()
    
    if args.interactive:
        interactive_mode(api)
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
            
            style = input("Style (auto/basic/advanced/formal/casual/corrected): ").strip() or "auto"
            
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

def print_help():
    """Print help information"""
    print("\nCommands:")
    print("  help    - Show this help")
    print("  styles  - Show available correction styles")
    print("  quit    - Exit the program")
    print("\nStyles:")
    print("  auto      - Auto-detect style (default)")
    print("  basic     - Basic correction")
    print("  advanced  - Advanced correction with context")
    print("  formal    - Formal/business style")
    print("  casual    - Casual/informal style")
    print("  corrected - Only fix typos and sentence structure")

if __name__ == "__main__":
    main() 