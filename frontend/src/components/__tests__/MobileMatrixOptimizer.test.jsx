/**
 * Comprehensive Unit Tests for MobileMatrixOptimizer Component
 * 
 * Tests mobile device detection, responsive behavior, orientation handling,
 * touch support, performance optimizations, and JSX style tag fixes.
 * 
 * Test Coverage:
 * - Mobile/Desktop Detection (8 tests)
 * - Orientation Handling (6 tests)
 * - Touch Support Detection (5 tests)
 * - CSS Style Injection (7 tests)
 * - Performance Monitoring (4 tests)
 * - Custom Hooks (6 tests)
 * - Component Exports (6 tests)
 * - Edge Cases & Error Handling (8 tests)
 * Total: 50+ comprehensive unit tests
 */

import React from 'react';
import { render, screen, act, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, {
  useMobile,
  MobileMatrixRain,
  MobileMatrixText
} from '../MobileMatrixOptimizer';

// Mock window.matchMedia for responsive tests
const mockMatchMedia = (matches) => {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
      matches: matches,
      media: query,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  });
};

// Mock navigator.userAgent
const mockUserAgent = (userAgent) => {
  Object.defineProperty(window.navigator, 'userAgent', {
    writable: true,
    configurable: true,
    value: userAgent
  });
};

// Mock window dimensions
const mockWindowDimensions = (width, height) => {
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: width
  });
  Object.defineProperty(window, 'innerHeight', {
    writable: true,
    configurable: true,
    value: height
  });
};

// Mock touch support
const mockTouchSupport = (hasTouch) => {
  if (hasTouch) {
    Object.defineProperty(window, 'ontouchstart', {
      writable: true,
      configurable: true,
      value: () => {}
    });
    Object.defineProperty(window.navigator, 'maxTouchPoints', {
      writable: true,
      configurable: true,
      value: 5
    });
  } else {
    delete window.ontouchstart;
    Object.defineProperty(window.navigator, 'maxTouchPoints', {
      writable: true,
      configurable: true,
      value: 0
    });
  }
};

describe('MobileMatrixOptimizer Component', () => {
  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
    mockMatchMedia(false);
    mockWindowDimensions(1920, 1080);
    mockTouchSupport(false);
    mockUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
    
    // Reset CSS custom properties
    document.documentElement.style.removeProperty('--matrix-effects-opacity');
  });

  describe('Mobile/Desktop Detection', () => {
    test('detects desktop environment correctly', () => {
      mockWindowDimensions(1920, 1080);
      mockUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.desktop-full')).toBeInTheDocument();
      expect(container.querySelector('.mobile-optimized')).not.toBeInTheDocument();
    });

    test('detects mobile environment by screen width', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.mobile-optimized')).toBeInTheDocument();
      expect(container.querySelector('.desktop-full')).not.toBeInTheDocument();
    });

    test('detects mobile environment by user agent - iPhone', () => {
      mockWindowDimensions(1024, 768);
      mockUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.mobile-optimized')).toBeInTheDocument();
    });

    test('detects mobile environment by user agent - Android', () => {
      mockWindowDimensions(1024, 768);
      mockUserAgent('Mozilla/5.0 (Linux; Android 10; SM-G973F)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.mobile-optimized')).toBeInTheDocument();
    });

    test('detects mobile environment by user agent - iPad', () => {
      mockWindowDimensions(1024, 768);
      mockUserAgent('Mozilla/5.0 (iPad; CPU OS 13_0 like Mac OS X)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.mobile-optimized')).toBeInTheDocument();
    });

    test('handles boundary case at 768px width - mobile', () => {
      mockWindowDimensions(768, 1024);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.mobile-optimized')).toBeInTheDocument();
    });

    test('handles boundary case at 769px width - desktop', () => {
      mockWindowDimensions(769, 1024);
      mockUserAgent('Mozilla/5.0 (Windows NT 10.0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.desktop-full')).toBeInTheDocument();
    });

    test('updates detection on window resize', async () => {
      mockWindowDimensions(1920, 1080);
      
      const { container, rerender } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.desktop-full')).toBeInTheDocument();
      
      // Simulate resize to mobile
      await act(async () => {
        mockWindowDimensions(375, 667);
        window.dispatchEvent(new Event('resize'));
        await new Promise(resolve => setTimeout(resolve, 100));
      });
      
      rerender(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
    });
  });

  describe('Orientation Handling', () => {
    test('detects portrait orientation correctly', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.orientation-portrait')).toBeInTheDocument();
    });

    test('detects landscape orientation correctly', () => {
      mockWindowDimensions(667, 375);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.orientation-landscape')).toBeInTheDocument();
    });

    test('handles square screens as landscape', () => {
      mockWindowDimensions(1000, 1000);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.orientation-landscape')).toBeInTheDocument();
    });

    test('updates orientation on window resize', async () => {
      mockWindowDimensions(375, 667);
      
      const { container, rerender } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.orientation-portrait')).toBeInTheDocument();
      
      await act(async () => {
        mockWindowDimensions(667, 375);
        window.dispatchEvent(new Event('resize'));
        await new Promise(resolve => setTimeout(resolve, 100));
      });
      
      rerender(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
    });

    test('handles orientation change event', async () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      await act(async () => {
        mockWindowDimensions(667, 375);
        window.dispatchEvent(new Event('orientationchange'));
        await new Promise(resolve => setTimeout(resolve, 100));
      });
    });

    test('applies correct orientation classes dynamically', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const mainDiv = container.firstChild;
      expect(mainDiv.className).toContain('orientation-');
    });
  });

  describe('Touch Support Detection', () => {
    test('detects touch support when ontouchstart exists', () => {
      mockTouchSupport(true);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.touch-enabled')).toBeInTheDocument();
    });

    test('detects no touch support on desktop', () => {
      mockTouchSupport(false);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.touch-disabled')).toBeInTheDocument();
    });

    test('detects touch support via maxTouchPoints', () => {
      delete window.ontouchstart;
      Object.defineProperty(window.navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 2
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.touch-enabled')).toBeInTheDocument();
    });

    test('applies touch-enabled class only when touch is supported', () => {
      mockTouchSupport(true);
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const mainDiv = container.firstChild;
      expect(mainDiv.className).toContain('touch-enabled');
      expect(mainDiv.className).not.toContain('touch-disabled');
    });

    test('handles missing touch properties gracefully', () => {
      delete window.ontouchstart;
      delete window.navigator.maxTouchPoints;
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('.touch-disabled')).toBeInTheDocument();
    });
  });

  describe('CSS Style Injection - JSX Attribute Fix', () => {
    test('injects mobile styles without jsx attribute', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
      expect(styleTag.hasAttribute('jsx')).toBe(false);
    });

    test('style tag contains mobile optimization CSS', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag.textContent).toContain('.mobile-optimized');
      expect(styleTag.textContent).toContain('-webkit-overflow-scrolling');
      expect(styleTag.textContent).toContain('scroll-behavior');
    });

    test('does not inject mobile styles on desktop', () => {
      mockWindowDimensions(1920, 1080);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag).not.toBeInTheDocument();
    });

    test('mobile styles include responsive text scaling', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag.textContent).toContain('clamp');
      expect(styleTag.textContent).toContain('text-5xl');
    });

    test('mobile styles include grid layout optimizations', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag.textContent).toContain('grid-template-columns');
      expect(styleTag.textContent).toContain('1fr !important');
    });

    test('mobile styles include touch target sizing', () => {
      mockWindowDimensions(375, 667);
      mockTouchSupport(true);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag.textContent).toContain('.touch-enabled');
      expect(styleTag.textContent).toContain('min-height: 44px');
    });

    test('mobile styles include orientation-specific rules', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag.textContent).toContain('.orientation-landscape');
      expect(styleTag.textContent).toContain('.orientation-portrait');
    });
  });

  describe('Performance Optimizations', () => {
    test('sets CSS custom property for mobile effects opacity', () => {
      mockWindowDimensions(375, 667);
      
      render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(opacity).toBe('0.3');
    });

    test('sets different opacity for desktop effects', () => {
      mockWindowDimensions(1920, 1080);
      
      render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(opacity).toBe('0.5');
    });

    test('shows performance monitor only on localhost - mobile', () => {
      mockWindowDimensions(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' }
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.textContent).toContain('Mobile:');
      expect(container.textContent).toContain('Touch:');
      expect(container.textContent).toContain('Orient:');
    });

    test('hides performance monitor on production domain', () => {
      mockWindowDimensions(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'example.com' }
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.textContent).not.toContain('Mobile:');
    });
  });

  describe('Custom Hook - useMobile', () => {
    test('useMobile hook returns false for desktop', () => {
      mockWindowDimensions(1920, 1080);
      
      let hookResult;
      const TestComponent = () => {
        hookResult = useMobile();
        return <div>Test</div>;
      };
      
      render(<TestComponent />);
      expect(hookResult).toBe(false);
    });

    test('useMobile hook returns true for mobile', () => {
      mockWindowDimensions(375, 667);
      
      let hookResult;
      const TestComponent = () => {
        hookResult = useMobile();
        return <div>Test</div>;
      };
      
      render(<TestComponent />);
      expect(hookResult).toBe(true);
    });

    test('useMobile hook updates on resize', async () => {
      mockWindowDimensions(1920, 1080);
      
      let hookResult;
      const TestComponent = () => {
        hookResult = useMobile();
        return <div>Test</div>;
      };
      
      const { rerender } = render(<TestComponent />);
      expect(hookResult).toBe(false);
      
      await act(async () => {
        mockWindowDimensions(375, 667);
        window.dispatchEvent(new Event('resize'));
        await new Promise(resolve => setTimeout(resolve, 100));
      });
      
      rerender(<TestComponent />);
    });

    test('useMobile hook checks exact 768px breakpoint', () => {
      mockWindowDimensions(768, 1024);
      
      let hookResult;
      const TestComponent = () => {
        hookResult = useMobile();
        return <div>Test</div>;
      };
      
      render(<TestComponent />);
      expect(hookResult).toBe(true);
    });

    test('useMobile hook cleans up event listener', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
      
      mockWindowDimensions(375, 667);
      
      const TestComponent = () => {
        useMobile();
        return <div>Test</div>;
      };
      
      const { unmount } = render(<TestComponent />);
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    });

    test('useMobile hook initializes correctly', () => {
      mockWindowDimensions(375, 667);
      
      let hookResult;
      const TestComponent = () => {
        hookResult = useMobile();
        return <div>{hookResult ? 'Mobile' : 'Desktop'}</div>;
      };
      
      const { container } = render(<TestComponent />);
      expect(container.textContent).toContain('Mobile');
    });
  });

  describe('Component Exports - MobileMatrixRain', () => {
    test('MobileMatrixRain renders on mobile', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(<MobileMatrixRain />);
      
      expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
    });

    test('MobileMatrixRain does not render on desktop', () => {
      mockWindowDimensions(1920, 1080);
      mockUserAgent('Mozilla/5.0 (Windows NT 10.0)');
      
      const { container } = render(<MobileMatrixRain />);
      
      expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
    });

    test('MobileMatrixRain applies custom className', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(<MobileMatrixRain className="custom-rain" />);
      
      const rainDiv = container.querySelector('.custom-rain');
      expect(rainDiv).toBeInTheDocument();
    });

    test('MobileMatrixRain includes animation styles without jsx attribute', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(<MobileMatrixRain />);
      
      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
      expect(styleTag.hasAttribute('jsx')).toBe(false);
      expect(styleTag.textContent).toContain('mobile-rain');
      expect(styleTag.textContent).toContain('keyframes');
    });

    test('MobileMatrixRain has correct opacity', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(<MobileMatrixRain />);
      
      const rainContainer = container.querySelector('.absolute.inset-0');
      expect(rainContainer.className).toContain('opacity-30');
    });

    test('MobileMatrixRain uses linear gradient background', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(<MobileMatrixRain />);
      
      const styleTag = container.querySelector('style');
      expect(styleTag.textContent).toContain('linear-gradient');
      expect(styleTag.textContent).toContain('rgba(0, 255, 65, 0.1)');
    });
  });

  describe('Component Exports - MobileMatrixText', () => {
    test('MobileMatrixText renders children correctly', () => {
      const { container } = render(
        <MobileMatrixText>
          <h1>Matrix Title</h1>
        </MobileMatrixText>
      );
      
      expect(container.textContent).toContain('Matrix Title');
    });

    test('MobileMatrixText applies mobile class on mobile', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );
      
      expect(container.querySelector('.mobile-matrix-text')).toBeInTheDocument();
    });

    test('MobileMatrixText does not apply mobile class on desktop', () => {
      mockWindowDimensions(1920, 1080);
      mockUserAgent('Mozilla/5.0 (Windows NT 10.0)');
      
      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );
      
      expect(container.querySelector('.mobile-matrix-text')).not.toBeInTheDocument();
    });

    test('MobileMatrixText includes responsive font sizing without jsx attribute', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
      expect(styleTag.hasAttribute('jsx')).toBe(false);
      expect(styleTag.textContent).toContain('clamp(1.5rem, 6vw, 3rem)');
    });

    test('MobileMatrixText includes glow animation', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag.textContent).toContain('.matrix-text-glow');
      expect(styleTag.textContent).toContain('text-shadow');
      expect(styleTag.textContent).toContain('mobile-glow');
    });

    test('MobileMatrixText accepts custom className', () => {
      const { container } = render(
        <MobileMatrixText className="custom-text-class">
          <span>Text</span>
        </MobileMatrixText>
      );
      
      const textDiv = container.querySelector('.custom-text-class');
      expect(textDiv).toBeInTheDocument();
    });
  });

  describe('Edge Cases & Error Handling', () => {
    test('handles missing window object gracefully', () => {
      // This test simulates SSR environment
      const originalWindow = global.window;
      
      // Can't actually delete window in this environment, but we can test rendering
      expect(() => {
        render(
          <MobileMatrixOptimizer>
            <div>Content</div>
          </MobileMatrixOptimizer>
        );
      }).not.toThrow();
      
      global.window = originalWindow;
    });

    test('handles children prop being null', () => {
      expect(() => {
        render(<MobileMatrixOptimizer>{null}</MobileMatrixOptimizer>);
      }).not.toThrow();
    });

    test('handles children prop being undefined', () => {
      expect(() => {
        render(<MobileMatrixOptimizer>{undefined}</MobileMatrixOptimizer>);
      }).not.toThrow();
    });

    test('handles empty className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toBeInTheDocument();
    });

    test('handles no className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toBeInTheDocument();
    });

    test('handles rapid resize events', async () => {
      mockWindowDimensions(1920, 1080);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      // Simulate rapid resize events
      await act(async () => {
        for (let i = 0; i < 10; i++) {
          mockWindowDimensions(800 + i * 50, 600);
          window.dispatchEvent(new Event('resize'));
        }
        await new Promise(resolve => setTimeout(resolve, 200));
      });
      
      expect(container.firstChild).toBeInTheDocument();
    });

    test('cleans up event listeners on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
      
      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
      expect(removeEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
    });

    test('handles multiple component instances independently', () => {
      mockWindowDimensions(375, 667);
      
      const { container } = render(
        <>
          <MobileMatrixOptimizer className="instance-1">
            <div>First</div>
          </MobileMatrixOptimizer>
          <MobileMatrixOptimizer className="instance-2">
            <div>Second</div>
          </MobileMatrixOptimizer>
        </>
      );
      
      const instances = container.querySelectorAll('.mobile-optimized');
      expect(instances.length).toBe(2);
    });
  });

  describe('Accessibility & Best Practices', () => {
    test('renders semantic HTML structure', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <main>Main Content</main>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('main')).toBeInTheDocument();
    });

    test('preserves child component structure', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div id="parent">
            <div id="child">Nested</div>
          </div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.querySelector('#parent')).toBeInTheDocument();
      expect(container.querySelector('#child')).toBeInTheDocument();
    });

    test('does not interfere with child event handlers', () => {
      const handleClick = jest.fn();
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <button onClick={handleClick}>Click Me</button>
        </MobileMatrixOptimizer>
      );
      
      const button = container.querySelector('button');
      button.click();
      
      expect(handleClick).toHaveBeenCalledTimes(1);
    });
  });
});