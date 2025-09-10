#!/usr/bin/env python3
"""
CSS Debug Utility for Research Aggregator
Helps verify CSS loading order and debug styling issues
"""

import os
import time
from pathlib import Path


def check_css_file():
    """Check if custom CSS file exists and show stats."""
    css_path = Path("static/custom.css")
    
    if not css_path.exists():
        print("❌ ERROR: static/custom.css not found!")
        print("   Create the file or check the path.")
        return False
    
    stat = css_path.stat()
    print(f"✅ CSS file found: {css_path}")
    print(f"   Size: {stat.st_size} bytes")
    print(f"   Modified: {time.ctime(stat.st_mtime)}")
    
    return True


def analyze_css_content():
    """Analyze CSS content for common issues."""
    css_path = Path("static/custom.css")
    
    if not css_path.exists():
        return
    
    with open(css_path, 'r') as f:
        content = f.read()
    
    print("\n📊 CSS Analysis:")
    print(f"   Total lines: {len(content.splitlines())}")
    print(f"   Total size: {len(content)} characters")
    
    # Count important declarations
    important_count = content.count('!important')
    print(f"   !important declarations: {important_count}")
    
    # Check for common selectors
    selectors = [
        '.gradio-container',
        '.paper-card',
        '.header-container',
        '[role="tab"]',
        '.search-container'
    ]
    
    print("\n🎯 Key Selectors Found:")
    for selector in selectors:
        count = content.count(selector)
        status = "✅" if count > 0 else "❌"
        print(f"   {status} {selector}: {count} occurrences")


def check_css_order_strategy():
    """Show the CSS loading strategy being used."""
    print("\n🔄 CSS Loading Strategy:")
    print("   1. Gradio default CSS loads first")
    print("   2. Gradio theme CSS loads second") 
    print("   3. Custom CSS injected via gr.HTML() - HIGHEST PRIORITY")
    print("   4. Runtime CSS overrides via JavaScript - ULTIMATE PRIORITY")
    print("   5. MutationObserver monitors and reapplies custom styles")


def generate_css_debug_snippet():
    """Generate JavaScript snippet for browser console debugging."""
    js_debug = """
// CSS Debug Tools - Paste in browser console

// 1. Check CSS loading order
const checkCSSOrder = () => {
    const stylesheets = Array.from(document.styleSheets);
    console.log('CSS Loading Order:');
    stylesheets.forEach((sheet, index) => {
        const href = sheet.href || 'inline';
        console.log(`${index + 1}. ${href}`);
    });
    
    const customCSS = document.getElementById('custom-css-override');
    const runtimeCSS = document.getElementById('runtime-overrides');
    console.log('Custom CSS element:', customCSS ? '✅ Found' : '❌ Missing');
    console.log('Runtime CSS element:', runtimeCSS ? '✅ Found' : '❌ Missing');
};

// 2. Check for conflicting styles
const checkConflicts = (selector) => {
    const elements = document.querySelectorAll(selector);
    if (elements.length === 0) {
        console.log(`No elements found for: ${selector}`);
        return;
    }
    
    elements.forEach((el, i) => {
        const styles = window.getComputedStyle(el);
        console.log(`Element ${i + 1}:`, {
            width: styles.width,
            maxWidth: styles.maxWidth,
            padding: styles.padding,
            margin: styles.margin
        });
    });
};

// 3. Force reapply custom styles
const forceCustomStyles = () => {
    const customCSS = document.getElementById('custom-css-override');
    if (customCSS) {
        document.head.appendChild(customCSS);
        console.log('✅ Custom CSS reapplied');
    } else {
        console.log('❌ Custom CSS not found');
    }
};

// 4. Test specific elements
const testElements = () => {
    checkConflicts('.gradio-container');
    checkConflicts('.paper-card');
    checkConflicts('[role="tab"]');
};

console.log('CSS Debug tools loaded. Available functions:');
console.log('- checkCSSOrder()');
console.log('- checkConflicts(selector)');
console.log('- forceCustomStyles()');
console.log('- testElements()');
"""
    
    print("\n🛠️  Browser Console Debug Tools:")
    print("   Copy and paste this into your browser console:")
    print("   " + "="*50)
    print(js_debug)
    print("   " + "="*50)


def main():
    """Main debug function."""
    print("🎨 CSS Debug Utility for Research Aggregator")
    print("=" * 50)
    
    # Check CSS file
    if not check_css_file():
        return
    
    # Analyze content
    analyze_css_content()
    
    # Show strategy
    check_css_order_strategy()
    
    # Generate debug tools
    generate_css_debug_snippet()
    
    print("\n✨ Debug complete! Your CSS should now have maximum priority.")
    print("   If styles aren't applying, use the browser console tools above.")


if __name__ == "__main__":
    main()
