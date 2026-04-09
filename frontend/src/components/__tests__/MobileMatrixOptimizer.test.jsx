/**
 * Unit tests for MobileMatrixOptimizer.jsx
 * Tests mobile detection, orientation handling, touch support, and responsive behavior
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
};

// Test component for useMobile hook
const TestMobileHook = () => {
  const isMobile = useMobile();
  return <div data-testid="mobile-status">{isMobile ? 'mobile' : 'desktop'}</div>;
};

describe('MobileMatrixOptimizer Component', () => {
  
  beforeEach(() => {
    // Reset to desktop defaults
    mockWindowProperties(1024, 768, 'Mozilla/5.0');
    jest.clearAllMocks();
  });

  describe('Desktop Rendering', () => {
    test('renders children correctly on desktop', () => {
      render(
        <MobileMatrixOptimizer>
          <div data-testid="child-content">Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByTestId('child-content')).toBeInTheDocument();
      expect(screen.getByText('Test Content')).toBeInTheDocument();
    });

    test('applies desktop-full class on desktop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="custom-class">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('custom-class');
      expect(wrapper).toHaveClass('desktop-full');
    });

    test('does not render mobile optimization styles on desktop', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styles = container.querySelector('style');
      expect(styles).not.toBeInTheDocument();
    });

    test('does not show performance monitor on desktop', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const monitor = container.querySelector('.fixed.bottom-2');
      expect(monitor).not.toBeInTheDocument();
    });
  });

  describe('Mobile Detection', () => {
    test('detects mobile by screen width (768px or less)', async () => {
      mockWindowProperties(768, 1024);
      
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

    test('detects mobile by user agent - iPhone', async () => {
      mockWindowProperties(1024, 768, 'iPhone');
      
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

    test('detects mobile by user agent - Android', async () => {
      mockWindowProperties(1024, 768, 'Android');
      
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

    test('detects mobile by user agent - iPad', async () => {
      mockWindowProperties(1024, 768, 'iPad');
      
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

    test('detects various mobile devices', async () => {
      const mobileUserAgents = [
        'iPhone',
        'iPad',
        'iPod',
        'Android',
        'BlackBerry',
        'IEMobile',
        'Opera Mini'
      ];

      for (const ua of mobileUserAgents) {
        mockWindowProperties(1024, 768, ua);
        
        const { container, unmount } = render(
          <MobileMatrixOptimizer>
            <div>Content</div>
          </MobileMatrixOptimizer>
        );

        await waitFor(() => {
          const wrapper = container.firstChild;
          expect(wrapper).toHaveClass('mobile-optimized');
        });

        unmount();
      }
    });
  });

  describe('Orientation Detection', () => {
    test('detects portrait orientation (height > width)', async () => {
      mockWindowProperties(375, 667); // iPhone portrait
      
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

    test('detects landscape orientation (width > height)', async () => {
      mockWindowProperties(667, 375); // iPhone landscape
      
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

    test('handles square aspect ratio as landscape', async () => {
      mockWindowProperties(600, 600);
      
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
        value: null,
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
        value: 0,
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

    test('detects touch via maxTouchPoints', async () => {
      delete window.ontouchstart;
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

      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('touch-enabled');
      });
    });
  });

  describe('Mobile Optimization Styles', () => {
    test('injects mobile optimization styles on mobile', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const style = container.querySelector('style');
        expect(style).toBeInTheDocument();
        expect(style.textContent).toContain('.mobile-optimized');
        expect(style.textContent).toContain('-webkit-overflow-scrolling');
      });
    });

    test('mobile styles include responsive text scaling', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const style = container.querySelector('style');
        expect(style.textContent).toContain('clamp(2rem, 8vw, 4rem)');
        expect(style.textContent).toContain('.text-5xl');
      });
    });

    test('mobile styles include grid optimizations', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const style = container.querySelector('style');
        expect(style.textContent).toContain('grid-template-columns: 1fr');
      });
    });

    test('mobile styles include touch target sizing', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const style = container.querySelector('style');
        expect(style.textContent).toContain('min-height: 44px');
        expect(style.textContent).toContain('min-width: 44px');
      });
    });

    test('uses standard style tag instead of styled-jsx', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const style = container.querySelector('style');
        expect(style).toBeInTheDocument();
        // Should not have jsx attribute
        expect(style.hasAttribute('jsx')).toBe(false);
      });
    });
  });

  describe('CSS Custom Properties', () => {
    test('sets matrix effects opacity for mobile', async () => {
      mockWindowProperties(375, 667);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const opacityValue = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
        expect(opacityValue).toBe('0.3');
      });
    });

    test('sets matrix effects opacity for desktop', async () => {
      mockWindowProperties(1024, 768);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const opacityValue = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
        expect(opacityValue).toBe('0.5');
      });
    });
  });

  describe('Performance Monitor', () => {
    test('shows performance monitor on localhost when mobile', async () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const monitor = container.querySelector('.fixed.bottom-2');
        expect(monitor).toBeInTheDocument();
      });
    });

    test('shows performance monitor on 127.0.0.1 when mobile', async () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: '127.0.0.1' },
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const monitor = container.querySelector('.fixed.bottom-2');
        expect(monitor).toBeInTheDocument();
      });
    });

    test('does not show performance monitor in production', async () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'example.com' },
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const monitor = container.querySelector('.fixed.bottom-2');
        expect(monitor).not.toBeInTheDocument();
      });
    });

    test('performance monitor displays correct mobile status', async () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const monitor = container.querySelector('.fixed.bottom-2');
        expect(monitor.textContent).toContain('Mobile: YES');
      });
    });

    test('performance monitor displays orientation', async () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const monitor = container.querySelector('.fixed.bottom-2');
        expect(monitor.textContent).toContain('Orient: PORTRAIT');
      });
    });

    test('performance monitor displays width', async () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const monitor = container.querySelector('.fixed.bottom-2');
        expect(monitor.textContent).toContain('Width: 375px');
      });
    });
  });

  describe('Event Listeners', () => {
    test('adds resize event listener', () => {
      const addEventListenerSpy = jest.spyOn(window, 'addEventListener');
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      expect(addEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    });

    test('adds orientationchange event listener', () => {
      const addEventListenerSpy = jest.spyOn(window, 'addEventListener');
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      expect(addEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
    });

    test('removes event listeners on unmount', () => {
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

    test('updates mobile state on window resize', async () => {
      mockWindowProperties(1024, 768);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('desktop-full');
      });

      // Simulate resize to mobile
      act(() => {
        mockWindowProperties(375, 667);
        window.dispatchEvent(new Event('resize'));
      });

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
    });
  });

  describe('Class Name Composition', () => {
    test('applies custom className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="custom-wrapper">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      expect(container.firstChild).toHaveClass('custom-wrapper');
    });

    test('combines multiple class names correctly', async () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window, 'ontouchstart', {
        value: null,
      });
      
      const { container } = render(
        <MobileMatrixOptimizer className="custom">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('custom');
        expect(wrapper).toHaveClass('mobile-optimized');
        expect(wrapper).toHaveClass('orientation-portrait');
        expect(wrapper).toHaveClass('touch-enabled');
      });
    });
  });
});

describe('useMobile Hook', () => {
  beforeEach(() => {
    mockWindowProperties(1024, 768);
    jest.clearAllMocks();
  });

  test('returns false for desktop width', async () => {
    mockWindowProperties(1024, 768);
    
    render(<TestMobileHook />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
    });
  });

  test('returns true for mobile width', async () => {
    mockWindowProperties(768, 1024);
    
    render(<TestMobileHook />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('returns true for width below 768px', async () => {
    mockWindowProperties(375, 667);
    
    render(<TestMobileHook />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('updates when window is resized', async () => {
    mockWindowProperties(1024, 768);
    
    render(<TestMobileHook />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
    });

    act(() => {
      mockWindowProperties(375, 667);
      window.dispatchEvent(new Event('resize'));
    });

    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('cleans up event listener on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    
    const { unmount } = render(<TestMobileHook />);
    unmount();

    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
  });
});

describe('MobileMatrixRain Component', () => {
  beforeEach(() => {
    mockWindowProperties(1024, 768);
    jest.clearAllMocks();
  });

  test('renders on mobile devices', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    await waitFor(() => {
      const rain = container.querySelector('.matrix-mobile-rain');
      expect(rain).toBeInTheDocument();
    });
  });

  test('does not render on desktop', async () => {
    mockWindowProperties(1024, 768);
    
    const { container } = render(<MobileMatrixRain />);
    
    await waitFor(() => {
      const rain = container.querySelector('.matrix-mobile-rain');
      expect(rain).not.toBeInTheDocument();
    });
  });

  test('applies custom className on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain className="custom-rain" />);
    
    await waitFor(() => {
      const wrapper = container.querySelector('.custom-rain');
      expect(wrapper).toBeInTheDocument();
    });
  });

  test('includes rain animation styles on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    await waitFor(() => {
      const style = container.querySelector('style');
      expect(style).toBeInTheDocument();
      expect(style.textContent).toContain('@keyframes mobile-rain');
      expect(style.textContent).toContain('linear-gradient');
    });
  });

  test('uses standard style tag instead of styled-jsx', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    await waitFor(() => {
      const style = container.querySelector('style');
      expect(style).toBeInTheDocument();
      expect(style.hasAttribute('jsx')).toBe(false);
    });
  });

  test('has pointer-events-none class', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    await waitFor(() => {
      const wrapper = container.querySelector('.pointer-events-none');
      expect(wrapper).toBeInTheDocument();
    });
  });

  test('returns null on desktop', () => {
    mockWindowProperties(1024, 768);
    
    const { container } = render(<MobileMatrixRain />);
    
    expect(container.firstChild).toBeNull();
  });
});

describe('MobileMatrixText Component', () => {
  beforeEach(() => {
    mockWindowProperties(1024, 768);
    jest.clearAllMocks();
  });

  test('renders children on all devices', () => {
    render(
      <MobileMatrixText>
        <span data-testid="text-content">Matrix Text</span>
      </MobileMatrixText>
    );
    
    expect(screen.getByTestId('text-content')).toBeInTheDocument();
    expect(screen.getByText('Matrix Text')).toBeInTheDocument();
  });

  test('applies mobile-matrix-text class on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Content</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-matrix-text');
    });
  });

  test('does not apply mobile-matrix-text class on desktop', async () => {
    mockWindowProperties(1024, 768);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Content</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      expect(container.firstChild).not.toHaveClass('mobile-matrix-text');
    });
  });

  test('injects mobile styles on mobile devices', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Content</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      const style = container.querySelector('style');
      expect(style).toBeInTheDocument();
      expect(style.textContent).toContain('.mobile-matrix-text');
      expect(style.textContent).toContain('clamp(1.5rem, 6vw, 3rem)');
    });
  });

  test('does not inject styles on desktop', () => {
    mockWindowProperties(1024, 768);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Content</span>
      </MobileMatrixText>
    );
    
    const style = container.querySelector('style');
    expect(style).not.toBeInTheDocument();
  });

  test('includes glow animation styles on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Content</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      const style = container.querySelector('style');
      expect(style.textContent).toContain('@keyframes mobile-glow');
      expect(style.textContent).toContain('text-shadow');
    });
  });

  test('uses standard style tag instead of styled-jsx', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Content</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      const style = container.querySelector('style');
      expect(style).toBeInTheDocument();
      expect(style.hasAttribute('jsx')).toBe(false);
    });
  });

  test('applies custom className', () => {
    const { container } = render(
      <MobileMatrixText className="custom-text">
        <span>Content</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).toHaveClass('custom-text');
  });

  test('combines custom and mobile classes on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText className="custom">
        <span>Content</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('custom');
      expect(container.firstChild).toHaveClass('mobile-matrix-text');
    });
  });
});

describe('Edge Cases and Error Handling', () => {
  beforeEach(() => {
    mockWindowProperties(1024, 768);
    jest.clearAllMocks();
  });

  test('handles undefined children gracefully', () => {
    expect(() => {
      render(<MobileMatrixOptimizer>{undefined}</MobileMatrixOptimizer>);
    }).not.toThrow();
  });

  test('handles null children gracefully', () => {
    expect(() => {
      render(<MobileMatrixOptimizer>{null}</MobileMatrixOptimizer>);
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

  test('handles missing className prop', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles rapid window resize events', async () => {
    mockWindowProperties(1024, 768);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    // Simulate rapid resizes
    for (let i = 0; i < 10; i++) {
      act(() => {
        mockWindowProperties(375 + i * 10, 667);
        window.dispatchEvent(new Event('resize'));
      });
    }

    await waitFor(() => {
      expect(container.firstChild).toBeInTheDocument();
    });
  });

  test('handles missing navigator.userAgent', async () => {
    Object.defineProperty(navigator, 'userAgent', {
      writable: true,
      configurable: true,
      value: undefined,
    });
    
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });

  test('handles missing navigator.maxTouchPoints', async () => {
    delete navigator.maxTouchPoints;
    
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });
});

describe('Responsive Breakpoints', () => {
  test('exact 768px width is considered mobile', async () => {
    mockWindowProperties(768, 1024);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  test('769px width is not considered mobile', async () => {
    mockWindowProperties(769, 1024);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    await waitFor(() => {
      expect(container.firstChild).toHaveClass('desktop-full');
    });
  });

  test('very small mobile width (320px)', async () => {
    mockWindowProperties(320, 568);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  test('tablet width (768px)', async () => {
    mockWindowProperties(768, 1024);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });
});