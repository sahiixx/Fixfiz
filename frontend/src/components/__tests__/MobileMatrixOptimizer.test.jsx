/**
 * Unit tests for MobileMatrixOptimizer.jsx
 * Tests mobile detection, responsive behavior, and JSX attribute fix
 * 
 * Note: This test file requires @testing-library/react and @testing-library/jest-dom
 * Install with: yarn add -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
 */

import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  useMobile, 
  MobileMatrixRain, 
  MobileMatrixText 
} from '../MobileMatrixOptimizer';

// Mock window.matchMedia
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

describe('MobileMatrixOptimizer', () => {
  // Store original window properties
  let originalInnerWidth;
  let originalInnerHeight;
  let originalUserAgent;

  beforeEach(() => {
    // Save original values
    originalInnerWidth = window.innerWidth;
    originalInnerHeight = window.innerHeight;
    originalUserAgent = navigator.userAgent;
    
    // Reset to desktop defaults
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 1024
    });
    Object.defineProperty(window, 'innerHeight', {
      writable: true,
      configurable: true,
      value: 768
    });
    
    mockMatchMedia(false);
  });

  afterEach(() => {
    // Restore original values
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: originalInnerWidth
    });
    Object.defineProperty(window, 'innerHeight', {
      writable: true,
      configurable: true,
      value: originalInnerHeight
    });
  });

  describe('Component Rendering', () => {
    test('renders children correctly', () => {
      render(
        <MobileMatrixOptimizer>
          <div data-testid="child-content">Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByTestId('child-content')).toBeInTheDocument();
      expect(screen.getByText('Test Content')).toBeInTheDocument();
    });

    test('applies custom className', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="custom-class">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('custom-class');
    });

    test('applies desktop classes on desktop viewport', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('desktop-full');
    });
  });

  describe('Mobile Detection', () => {
    test('detects mobile viewport width (<=768px)', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('mobile-optimized');
      });
    });

    test('detects mobile user agent', async () => {
      Object.defineProperty(navigator, 'userAgent', {
        writable: true,
        configurable: true,
        value: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('mobile-optimized');
      });
    });

    test('detects tablet viewport (768px)', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 768
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const wrapper = container.firstChild;
        // At exactly 768px, should be treated as mobile
        expect(wrapper).toHaveClass('mobile-optimized');
      });
    });
  });

  describe('Orientation Detection', () => {
    test('detects portrait orientation', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 667
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('orientation-portrait');
      });
    });

    test('detects landscape orientation', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 667
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 375
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('orientation-landscape');
      });
    });
  });

  describe('Touch Support Detection', () => {
    test('detects touch support', async () => {
      Object.defineProperty(window, 'ontouchstart', {
        writable: true,
        configurable: true,
        value: null
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('touch-enabled');
      });
    });

    test('detects no touch support', async () => {
      delete window.ontouchstart;
      Object.defineProperty(navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 0
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('touch-disabled');
      });
    });
  });

  describe('Style Injection - JSX Attribute Fix', () => {
    test('injects mobile optimization styles without jsx attribute warning', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        // Check that style element exists
        const styleElement = container.querySelector('style');
        expect(styleElement).toBeInTheDocument();
        
        // Verify it's a standard <style> tag, not <style jsx>
        expect(styleElement.getAttribute('jsx')).toBeNull();
        
        // Verify style content includes mobile optimizations
        const styleContent = styleElement.textContent;
        expect(styleContent).toContain('.mobile-optimized');
        expect(styleContent).toContain('-webkit-overflow-scrolling: touch');
      });
    });

    test('does not inject mobile styles on desktop', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      // Style element should not be present on desktop
      const styleElement = container.querySelector('style');
      expect(styleElement).not.toBeInTheDocument();
    });

    test('style element has correct CSS for responsive text', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const styleElement = container.querySelector('style');
        const styleContent = styleElement.textContent;
        
        // Check for responsive text scaling
        expect(styleContent).toContain('font-size: clamp');
        expect(styleContent).toContain('.text-5xl');
        expect(styleContent).toContain('.text-6xl');
        expect(styleContent).toContain('.text-7xl');
      });
    });

    test('style element has correct CSS for touch targets', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });
      Object.defineProperty(window, 'ontouchstart', {
        writable: true,
        configurable: true,
        value: null
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const styleElement = container.querySelector('style');
        const styleContent = styleElement.textContent;
        
        // Check for touch target sizing
        expect(styleContent).toContain('.touch-enabled button');
        expect(styleContent).toContain('min-height: 44px');
        expect(styleContent).toContain('min-width: 44px');
      });
    });
  });

  describe('Performance Monitor', () => {
    test('shows performance monitor on localhost', async () => {
      Object.defineProperty(window, 'location', {
        writable: true,
        configurable: true,
        value: {
          ...window.location,
          hostname: 'localhost'
        }
      });
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });

      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
        expect(screen.getByText(/Touch:/)).toBeInTheDocument();
        expect(screen.getByText(/Orient:/)).toBeInTheDocument();
        expect(screen.getByText(/Width:/)).toBeInTheDocument();
      });
    });

    test('hides performance monitor on production', async () => {
      Object.defineProperty(window, 'location', {
        writable: true,
        configurable: true,
        value: {
          ...window.location,
          hostname: 'create-25.preview.emergentagent.com'
        }
      });
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });

      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
      });
    });

    test('performance monitor on 127.0.0.1', async () => {
      Object.defineProperty(window, 'location', {
        writable: true,
        configurable: true,
        value: {
          ...window.location,
          hostname: '127.0.0.1'
        }
      });
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });

      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
      });
    });
  });

  describe('Event Listeners', () => {
    test('responds to window resize event', async () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      // Start on desktop
      expect(container.firstChild).toHaveClass('desktop-full');

      // Resize to mobile
      act(() => {
        Object.defineProperty(window, 'innerWidth', {
          writable: true,
          configurable: true,
          value: 375
        });
        window.dispatchEvent(new Event('resize'));
      });

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
    });

    test('responds to orientation change event', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 667
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-portrait');
      });

      // Simulate orientation change
      act(() => {
        const temp = window.innerWidth;
        Object.defineProperty(window, 'innerWidth', {
          writable: true,
          configurable: true,
          value: window.innerHeight
        });
        Object.defineProperty(window, 'innerHeight', {
          writable: true,
          configurable: true,
          value: temp
        });
        window.dispatchEvent(new Event('orientationchange'));
      });

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-landscape');
      });
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
      
      removeEventListenerSpy.mockRestore();
    });
  });

  describe('CSS Custom Properties', () => {
    test('sets matrix effects opacity for mobile', async () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375
      });

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
  });
});

describe('useMobile Hook', () => {
  const TestComponent = () => {
    const isMobile = useMobile();
    return <div data-testid="mobile-status">{isMobile ? 'mobile' : 'desktop'}</div>;
  };

  test('returns false for desktop viewport', () => {
    render(<TestComponent />);
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
  });

  test('returns true for mobile viewport', async () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    render(<TestComponent />);

    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('updates on window resize', async () => {
    render(<TestComponent />);
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');

    act(() => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 500
      });
      window.dispatchEvent(new Event('resize'));
    });

    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });
});

describe('MobileMatrixRain Component', () => {
  test('renders on mobile devices', async () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    const { container } = render(<MobileMatrixRain />);

    await waitFor(() => {
      const rainElement = container.querySelector('.matrix-mobile-rain');
      expect(rainElement).toBeInTheDocument();
    });
  });

  test('does not render on desktop', () => {
    const { container } = render(<MobileMatrixRain />);
    
    const rainElement = container.querySelector('.matrix-mobile-rain');
    expect(rainElement).not.toBeInTheDocument();
  });

  test('applies custom className', async () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    const { container } = render(<MobileMatrixRain className="custom-rain" />);

    await waitFor(() => {
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('custom-rain');
    });
  });

  test('injects animation styles without jsx attribute', async () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    const { container } = render(<MobileMatrixRain />);

    await waitFor(() => {
      const styleElement = container.querySelector('style');
      expect(styleElement).toBeInTheDocument();
      expect(styleElement.getAttribute('jsx')).toBeNull();
      
      const styleContent = styleElement.textContent;
      expect(styleContent).toContain('@keyframes mobile-rain');
      expect(styleContent).toContain('linear-gradient');
    });
  });

  test('has correct opacity and pointer-events', async () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    const { container } = render(<MobileMatrixRain />);

    await waitFor(() => {
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('opacity-30');
      expect(wrapper).toHaveClass('pointer-events-none');
    });
  });
});

describe('MobileMatrixText Component', () => {
  test('renders children correctly', () => {
    render(
      <MobileMatrixText>
        <span data-testid="text-content">Matrix Text</span>
      </MobileMatrixText>
    );
    
    expect(screen.getByTestId('text-content')).toBeInTheDocument();
    expect(screen.getByText('Matrix Text')).toBeInTheDocument();
  });

  test('applies mobile-matrix-text class on mobile', async () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );

    await waitFor(() => {
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('mobile-matrix-text');
    });
  });

  test('does not apply mobile-matrix-text class on desktop', () => {
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );

    const wrapper = container.firstChild;
    expect(wrapper).not.toHaveClass('mobile-matrix-text');
  });

  test('injects mobile text styles without jsx attribute', async () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );

    await waitFor(() => {
      const styleElement = container.querySelector('style');
      expect(styleElement).toBeInTheDocument();
      expect(styleElement.getAttribute('jsx')).toBeNull();
      
      const styleContent = styleElement.textContent;
      expect(styleContent).toContain('.mobile-matrix-text');
      expect(styleContent).toContain('font-size: clamp');
      expect(styleContent).toContain('text-shadow');
      expect(styleContent).toContain('@keyframes mobile-glow');
    });
  });

  test('applies custom className', () => {
    const { container } = render(
      <MobileMatrixText className="custom-text">
        <span>Text</span>
      </MobileMatrixText>
    );

    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('custom-text');
  });

  test('does not inject styles on desktop', () => {
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );

    const styleElement = container.querySelector('style');
    expect(styleElement).not.toBeInTheDocument();
  });
});

describe('Edge Cases and Error Handling', () => {
  test('handles missing children gracefully', () => {
    const { container } = render(<MobileMatrixOptimizer />);
    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles undefined className', () => {
    const { container } = render(
      <MobileMatrixOptimizer className={undefined}>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles null children', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        {null}
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles rapid viewport changes', async () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    // Rapid resize events
    for (let i = 0; i < 10; i++) {
      act(() => {
        Object.defineProperty(window, 'innerWidth', {
          writable: true,
          configurable: true,
          value: i % 2 === 0 ? 375 : 1024
        });
        window.dispatchEvent(new Event('resize'));
      });
    }

    await waitFor(() => {
      // Should still be in a valid state
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass(/mobile-optimized|desktop-full/);
    });
  });
});

describe('Integration Tests', () => {
  test('all mobile optimizations work together', async () => {
    Object.defineProperty(window, 'location', {
      writable: true,
      configurable: true,
      value: {
        ...window.location,
        hostname: 'localhost'
      }
    });
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });
    Object.defineProperty(window, 'innerHeight', {
      writable: true,
      configurable: true,
      value: 667
    });
    Object.defineProperty(window, 'ontouchstart', {
      writable: true,
      configurable: true,
      value: null
    });

    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    await waitFor(() => {
      const wrapper = container.firstChild;
      
      // Check all mobile classes are applied
      expect(wrapper).toHaveClass('mobile-optimized');
      expect(wrapper).toHaveClass('orientation-portrait');
      expect(wrapper).toHaveClass('touch-enabled');
      
      // Check styles are injected
      const styleElement = container.querySelector('style');
      expect(styleElement).toBeInTheDocument();
      expect(styleElement.getAttribute('jsx')).toBeNull();
      
      // Check performance monitor is visible
      expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
      
      // Check CSS custom property
      const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(opacity).toBe('0.3');
    });
  });

  test('works with MobileMatrixRain and MobileMatrixText together', async () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    const { container } = render(
      <MobileMatrixOptimizer>
        <MobileMatrixRain />
        <MobileMatrixText>
          <h1>Mobile Matrix</h1>
        </MobileMatrixText>
      </MobileMatrixOptimizer>
    );

    await waitFor(() => {
      // Check both components rendered
      expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
      expect(screen.getByText('Mobile Matrix')).toBeInTheDocument();
      
      // Check both have styles without jsx attribute
      const styleElements = container.querySelectorAll('style');
      expect(styleElements.length).toBeGreaterThan(0);
      styleElements.forEach(style => {
        expect(style.getAttribute('jsx')).toBeNull();
      });
    });
  });
});