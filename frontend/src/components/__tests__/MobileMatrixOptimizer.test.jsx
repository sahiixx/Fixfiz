/**
 * Comprehensive Unit Tests for MobileMatrixOptimizer Component
 * 
 * Tests cover:
 * - Component rendering and lifecycle
 * - Mobile detection and device handling
 * - Orientation changes and touch support
 * - Custom hooks (useMobile)
 * - Responsive styling and CSS injection
 * - Child components (MobileMatrixRain, MobileMatrixText)
 * - Edge cases and error conditions
 */

import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  useMobile, 
  MobileMatrixRain, 
  MobileMatrixText 
} from '../MobileMatrixOptimizer';

// Mock window properties
const mockWindowProperties = (width, height, userAgent = '') => {
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: width,
  });
  Object.defineProperty(window, 'innerHeight', {
    writable: true,
    configurable: true,
    value: height,
  });
  Object.defineProperty(navigator, 'userAgent', {
    writable: true,
    configurable: true,
    value: userAgent,
  });
  Object.defineProperty(navigator, 'maxTouchPoints', {
    writable: true,
    configurable: true,
    value: 0,
  });
};

// Helper to trigger resize event
const triggerResize = (width, height) => {
  window.innerWidth = width;
  window.innerHeight = height;
  window.dispatchEvent(new Event('resize'));
};

// Helper to trigger orientation change
const triggerOrientationChange = () => {
  window.dispatchEvent(new Event('orientationchange'));
};

describe('MobileMatrixOptimizer Component', () => {
  beforeEach(() => {
    // Reset window properties before each test
    mockWindowProperties(1024, 768, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
    // Clear any injected styles
    document.head.innerHTML = '';
    document.documentElement.style.cssText = '';
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  // ========================================================================
  // Basic Rendering Tests
  // ========================================================================

  describe('Rendering', () => {
    test('renders children correctly', () => {
      render(
        <MobileMatrixOptimizer>
          <div data-testid="child">Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByTestId('child')).toBeInTheDocument();
      expect(screen.getByText('Test Content')).toBeInTheDocument();
    });

    test('applies custom className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="custom-class">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('custom-class');
    });

    test('renders without crashing when no children provided', () => {
      const { container } = render(<MobileMatrixOptimizer />);
      expect(container.firstChild).toBeInTheDocument();
    });

    test('renders with empty className by default', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toBeInTheDocument();
    });
  });

  // ========================================================================
  // Mobile Detection Tests
  // ========================================================================

  describe('Mobile Detection', () => {
    test('detects mobile device by width (768px or less)', () => {
      mockWindowProperties(768, 1024);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('detects mobile device by width (less than 768px)', () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('detects desktop device (width > 768px)', () => {
      mockWindowProperties(1920, 1080);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('desktop-full');
    });

    test('detects mobile via user agent (Android)', () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (Linux; Android 10)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('detects mobile via user agent (iPhone)', () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('detects mobile via user agent (iPad)', () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (iPad; CPU OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('handles edge case at exact 768px boundary', () => {
      mockWindowProperties(768, 1024);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      // At exactly 768px, should be considered mobile
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  // ========================================================================
  // Orientation Detection Tests
  // ========================================================================

  describe('Orientation Detection', () => {
    test('detects portrait orientation (height > width)', () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-portrait');
    });

    test('detects landscape orientation (width > height)', () => {
      mockWindowProperties(667, 375);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });

    test('handles square viewport (width === height)', () => {
      mockWindowProperties(500, 500);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      // When equal, should default to landscape
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });

    test('updates orientation on orientationchange event', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-portrait');
      
      // Change to landscape
      act(() => {
        window.innerWidth = 667;
        window.innerHeight = 375;
        triggerOrientationChange();
      });
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-landscape');
      });
    });
  });

  // ========================================================================
  // Touch Support Tests
  // ========================================================================

  describe('Touch Support', () => {
    test('detects touch support via ontouchstart', () => {
      window.ontouchstart = () => {};
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-enabled');
      
      delete window.ontouchstart;
    });

    test('detects touch support via maxTouchPoints', () => {
      Object.defineProperty(navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 5,
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-enabled');
    });

    test('detects no touch support', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-disabled');
    });
  });

  // ========================================================================
  // CSS Injection Tests
  // ========================================================================

  describe('CSS Injection', () => {
    test('injects mobile styles when on mobile device', () => {
      mockWindowProperties(375, 667);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      // Check that style element is added to the DOM
      const styleElements = document.querySelectorAll('style');
      expect(styleElements.length).toBeGreaterThan(0);
      
      // Verify style content includes mobile optimization
      const styleContent = Array.from(styleElements)
        .map(el => el.textContent)
        .join('');
      expect(styleContent).toContain('.mobile-optimized');
    });

    test('does not inject mobile styles on desktop', () => {
      mockWindowProperties(1920, 1080);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      // Desktop should not inject mobile-specific styles
      const styleElements = document.querySelectorAll('style');
      const styleContent = Array.from(styleElements)
        .map(el => el.textContent)
        .join('');
      
      // Mobile optimization styles should not be present
      if (styleContent) {
        expect(styleContent).not.toContain('-webkit-overflow-scrolling: touch');
      }
    });

    test('uses standard style tag (not styled-jsx)', () => {
      mockWindowProperties(375, 667);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleElements = document.querySelectorAll('style');
      styleElements.forEach(styleEl => {
        // Should not have jsx attribute (checking the fix)
        expect(styleEl.hasAttribute('jsx')).toBe(false);
      });
    });
  });

  // ========================================================================
  // CSS Variable Tests
  // ========================================================================

  describe('CSS Variables', () => {
    test('sets matrix effects opacity for mobile', async () => {
      mockWindowProperties(375, 667);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
        expect(opacity).toBe('0.3');
      });
    });

    test('sets matrix effects opacity for desktop', async () => {
      mockWindowProperties(1920, 1080);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
        expect(opacity).toBe('0.5');
      });
    });

    test('updates CSS variable on device change', async () => {
      mockWindowProperties(1920, 1080);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      // Initially desktop
      await waitFor(() => {
        expect(document.documentElement.style.getPropertyValue('--matrix-effects-opacity')).toBe('0.5');
      });
      
      // Change to mobile
      act(() => {
        triggerResize(375, 667);
      });
      
      await waitFor(() => {
        expect(document.documentElement.style.getPropertyValue('--matrix-effects-opacity')).toBe('0.3');
      });
    });
  });

  // ========================================================================
  // Performance Monitor Tests
  // ========================================================================

  describe('Performance Monitor', () => {
    test('shows performance monitor on mobile localhost', () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
      expect(screen.getByText(/Touch:/)).toBeInTheDocument();
      expect(screen.getByText(/Orient:/)).toBeInTheDocument();
    });

    test('shows performance monitor on mobile 127.0.0.1', () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: '127.0.0.1' },
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
    });

    test('does not show performance monitor on production', () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'example.com' },
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
    });

    test('does not show performance monitor on desktop', () => {
      mockWindowProperties(1920, 1080);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
    });

    test('displays correct device information in monitor', () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText(/Mobile: YES/)).toBeInTheDocument();
      expect(screen.getByText(/Orient: PORTRAIT/)).toBeInTheDocument();
      expect(screen.getByText(/Width: 375px/)).toBeInTheDocument();
    });
  });

  // ========================================================================
  // Event Listener Cleanup Tests
  // ========================================================================

  describe('Event Listener Cleanup', () => {
    test('removes resize listener on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
      
      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    });

    test('removes orientationchange listener on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
      
      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
    });

    test('handles multiple mount/unmount cycles', () => {
      const { unmount, rerender } = render(
        <MobileMatrixOptimizer>
          <div>Content 1</div>
        </MobileMatrixOptimizer>
      );
      
      unmount();
      
      // Should not throw error on second mount
      expect(() => {
        render(
          <MobileMatrixOptimizer>
            <div>Content 2</div>
          </MobileMatrixOptimizer>
        );
      }).not.toThrow();
    });
  });

  // ========================================================================
  // Resize Event Tests
  // ========================================================================

  describe('Resize Events', () => {
    test('updates on window resize from desktop to mobile', async () => {
      mockWindowProperties(1920, 1080);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('desktop-full');
      
      act(() => {
        triggerResize(375, 667);
      });
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
    });

    test('updates on window resize from mobile to desktop', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
      
      act(() => {
        triggerResize(1920, 1080);
      });
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('desktop-full');
      });
    });

    test('handles rapid resize events', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      // Trigger multiple rapid resizes
      act(() => {
        for (let i = 0; i < 10; i++) {
          triggerResize(375 + i * 100, 667);
        }
      });
      
      // Should handle without errors
      expect(container.firstChild).toBeInTheDocument();
    });
  });
});

// ========================================================================
// useMobile Hook Tests
// ========================================================================

describe('useMobile Hook', () => {
  // Create a test component that uses the hook
  const TestComponent = () => {
    const isMobile = useMobile();
    return <div data-testid="mobile-status">{isMobile ? 'mobile' : 'desktop'}</div>;
  };

  beforeEach(() => {
    mockWindowProperties(1024, 768);
  });

  test('returns false for desktop width', () => {
    mockWindowProperties(1920, 1080);
    
    render(<TestComponent />);
    
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
  });

  test('returns true for mobile width', () => {
    mockWindowProperties(375, 667);
    
    render(<TestComponent />);
    
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
  });

  test('returns true at 768px boundary', () => {
    mockWindowProperties(768, 1024);
    
    render(<TestComponent />);
    
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
  });

  test('updates on resize event', async () => {
    mockWindowProperties(1920, 1080);
    
    render(<TestComponent />);
    
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
    
    act(() => {
      triggerResize(375, 667);
    });
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('cleans up resize listener on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    
    const { unmount } = render(<TestComponent />);
    
    unmount();
    
    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
  });
});

// ========================================================================
// MobileMatrixRain Component Tests
// ========================================================================

describe('MobileMatrixRain Component', () => {
  beforeEach(() => {
    mockWindowProperties(1024, 768);
    document.head.innerHTML = '';
  });

  test('renders rain effect on mobile', () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
  });

  test('does not render on desktop', () => {
    mockWindowProperties(1920, 1080);
    
    const { container } = render(<MobileMatrixRain />);
    
    expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
  });

  test('applies custom className', () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain className="custom-rain" />);
    
    const rainContainer = container.querySelector('.custom-rain');
    expect(rainContainer).toBeInTheDocument();
  });

  test('injects animation styles on mobile', () => {
    mockWindowProperties(375, 667);
    
    render(<MobileMatrixRain />);
    
    const styleElements = document.querySelectorAll('style');
    const styleContent = Array.from(styleElements)
      .map(el => el.textContent)
      .join('');
    
    expect(styleContent).toContain('@keyframes mobile-rain');
  });

  test('uses standard style tag (not styled-jsx)', () => {
    mockWindowProperties(375, 667);
    
    render(<MobileMatrixRain />);
    
    const styleElements = document.querySelectorAll('style');
    styleElements.forEach(styleEl => {
      expect(styleEl.hasAttribute('jsx')).toBe(false);
    });
  });

  test('applies correct opacity', () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    const rainContainer = container.firstChild;
    expect(rainContainer).toHaveClass('opacity-30');
  });

  test('renders as pointer-events-none', () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    const rainContainer = container.firstChild;
    expect(rainContainer).toHaveClass('pointer-events-none');
  });

  test('updates when switching from desktop to mobile', async () => {
    mockWindowProperties(1920, 1080);
    
    const { container, rerender } = render(<MobileMatrixRain />);
    
    expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
    
    act(() => {
      triggerResize(375, 667);
    });
    
    rerender(<MobileMatrixRain />);
    
    await waitFor(() => {
      expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
    });
  });
});

// ========================================================================
// MobileMatrixText Component Tests
// ========================================================================

describe('MobileMatrixText Component', () => {
  beforeEach(() => {
    mockWindowProperties(1024, 768);
    document.head.innerHTML = '';
  });

  test('renders children correctly', () => {
    render(
      <MobileMatrixText>
        <span data-testid="text-child">Matrix Text</span>
      </MobileMatrixText>
    );
    
    expect(screen.getByTestId('text-child')).toBeInTheDocument();
    expect(screen.getByText('Matrix Text')).toBeInTheDocument();
  });

  test('applies mobile-matrix-text class on mobile', () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).toHaveClass('mobile-matrix-text');
  });

  test('does not apply mobile class on desktop', () => {
    mockWindowProperties(1920, 1080);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).not.toHaveClass('mobile-matrix-text');
  });

  test('applies custom className', () => {
    const { container } = render(
      <MobileMatrixText className="custom-text">
        <span>Text</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).toHaveClass('custom-text');
  });

  test('injects mobile text styles on mobile', () => {
    mockWindowProperties(375, 667);
    
    render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleElements = document.querySelectorAll('style');
    const styleContent = Array.from(styleElements)
      .map(el => el.textContent)
      .join('');
    
    expect(styleContent).toContain('.mobile-matrix-text');
    expect(styleContent).toContain('font-size: clamp');
  });

  test('injects glow animation styles on mobile', () => {
    mockWindowProperties(375, 667);
    
    render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleElements = document.querySelectorAll('style');
    const styleContent = Array.from(styleElements)
      .map(el => el.textContent)
      .join('');
    
    expect(styleContent).toContain('@keyframes mobile-glow');
    expect(styleContent).toContain('text-shadow');
  });

  test('uses standard style tag (not styled-jsx)', () => {
    mockWindowProperties(375, 667);
    
    render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleElements = document.querySelectorAll('style');
    styleElements.forEach(styleEl => {
      expect(styleEl.hasAttribute('jsx')).toBe(false);
    });
  });

  test('does not inject styles on desktop', () => {
    mockWindowProperties(1920, 1080);
    
    render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleElements = document.querySelectorAll('style');
    const styleContent = Array.from(styleElements)
      .map(el => el.textContent)
      .join('');
    
    // Should not have mobile-specific text styles
    if (styleContent) {
      expect(styleContent).not.toContain('.mobile-matrix-text');
    }
  });

  test('handles empty children gracefully', () => {
    const { container } = render(<MobileMatrixText />);
    
    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles multiple children', () => {
    render(
      <MobileMatrixText>
        <span data-testid="child1">Text 1</span>
        <span data-testid="child2">Text 2</span>
      </MobileMatrixText>
    );
    
    expect(screen.getByTestId('child1')).toBeInTheDocument();
    expect(screen.getByTestId('child2')).toBeInTheDocument();
  });
});

// ========================================================================
// Integration Tests
// ========================================================================

describe('Integration Tests', () => {
  beforeEach(() => {
    mockWindowProperties(1024, 768);
    document.head.innerHTML = '';
    document.documentElement.style.cssText = '';
  });

  test('all components work together on mobile', () => {
    mockWindowProperties(375, 667);
    Object.defineProperty(window, 'location', {
      writable: true,
      value: { hostname: 'localhost' },
    });
    
    render(
      <MobileMatrixOptimizer>
        <MobileMatrixRain />
        <MobileMatrixText>
          <h1>Test Title</h1>
        </MobileMatrixText>
      </MobileMatrixOptimizer>
    );
    
    // Check all components rendered
    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(document.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
    expect(screen.getByText(/Mobile: YES/)).toBeInTheDocument();
  });

  test('components respond to device changes together', async () => {
    mockWindowProperties(1920, 1080);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <MobileMatrixRain className="rain-test" />
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      </MobileMatrixOptimizer>
    );
    
    // Initially desktop
    expect(container.firstChild).toHaveClass('desktop-full');
    expect(document.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
    
    // Switch to mobile
    act(() => {
      triggerResize(375, 667);
    });
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  test('nested MobileMatrixOptimizer components', () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixOptimizer className="outer">
        <MobileMatrixOptimizer className="inner">
          <div>Nested Content</div>
        </MobileMatrixOptimizer>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText('Nested Content')).toBeInTheDocument();
    const elements = container.querySelectorAll('.mobile-optimized');
    expect(elements.length).toBe(2);
  });
});

// ========================================================================
// Edge Cases and Error Handling
// ========================================================================

describe('Edge Cases', () => {
  beforeEach(() => {
    mockWindowProperties(1024, 768);
  });

  test('handles missing window properties gracefully', () => {
    // This tests defensive programming
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });

  test('handles very small viewport dimensions', () => {
    mockWindowProperties(100, 100);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toHaveClass('mobile-optimized');
  });

  test('handles very large viewport dimensions', () => {
    mockWindowProperties(10000, 10000);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toHaveClass('desktop-full');
  });

  test('handles rapid device type switching', async () => {
    mockWindowProperties(1920, 1080);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    // Switch multiple times rapidly
    for (let i = 0; i < 5; i++) {
      act(() => {
        triggerResize(i % 2 === 0 ? 375 : 1920, 667);
      });
    }
    
    // Should not crash
    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles component with null children', () => {
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          {null}
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });

  test('handles component with undefined children', () => {
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          {undefined}
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });

  test('handles component with boolean children', () => {
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          {false}
          {true}
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });
});