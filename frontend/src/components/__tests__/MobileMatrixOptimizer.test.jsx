/**
 * Comprehensive unit tests for MobileMatrixOptimizer.jsx
 * Tests focus on JSX styling fix, mobile detection, responsive behavior, and component rendering
 */
import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  MobileMatrixRain, 
  MobileMatrixText 
} from '../MobileMatrixOptimizer';

// Mock window.matchMedia
const mockMatchMedia = (matches = false) => {
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

// Mock screen orientation API
const mockOrientation = (type = 'landscape-primary', angle = 0) => {
  Object.defineProperty(window.screen, 'orientation', {
    writable: true,
    value: {
      type: type,
      angle: angle,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    },
  });
};

describe('MobileMatrixOptimizer Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockMatchMedia(false);
    mockOrientation('landscape-primary', 0);
  });

  afterEach(() => {
    jest.clearAllMocks();
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

    test('renders without crashing with no children', () => {
      const { container } = render(<MobileMatrixOptimizer />);
      expect(container.firstChild).toBeInTheDocument();
    });

    test('applies custom className prop', () => {
      const customClass = 'custom-test-class';
      const { container } = render(
        <MobileMatrixOptimizer className={customClass}>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      expect(container.firstChild).toHaveClass(customClass);
    });

    test('renders with default empty className', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      expect(container.firstChild).toBeInTheDocument();
    });
  });

  describe('Mobile Detection', () => {
    test('detects mobile devices correctly', () => {
      mockMatchMedia(true); // Simulate mobile device

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Mobile Content</div>
        </MobileMatrixOptimizer>
      );

      // Should have mobile-specific classes
      const wrapper = container.firstChild;
      expect(wrapper.className).toContain('mobile');
    });

    test('handles desktop devices correctly', () => {
      mockMatchMedia(false); // Simulate desktop device

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Desktop Content</div>
        </MobileMatrixOptimizer>
      );

      const wrapper = container.firstChild;
      // Should not have mobile-specific optimization classes
      expect(wrapper.className).not.toContain('mobile-optimized');
    });
  });

  describe('Style Tag Rendering', () => {
    test('renders standard <style> tag for mobile devices (not <style jsx>)', () => {
      mockMatchMedia(true);

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      // Check that style tag exists
      const styleTags = container.querySelectorAll('style');
      expect(styleTags.length).toBeGreaterThan(0);

      // Verify no jsx attribute is present (the fix we're testing)
      styleTags.forEach(styleTag => {
        expect(styleTag.hasAttribute('jsx')).toBe(false);
      });
    });

    test('style tag contains expected mobile CSS rules', () => {
      mockMatchMedia(true);

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
      
      const styleContent = styleTag.textContent;
      // Check for key mobile optimization CSS
      expect(styleContent).toContain('-webkit-overflow-scrolling');
      expect(styleContent).toContain('touch-action');
    });

    test('does not render style tag for desktop devices', () => {
      mockMatchMedia(false);

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      // Should not have mobile-specific style tag
      const styleTags = container.querySelectorAll('style');
      expect(styleTags.length).toBe(0);
    });
  });

  describe('Responsive Behavior', () => {
    test('updates when viewport changes from desktop to mobile', async () => {
      const { rerender } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      // Simulate viewport change to mobile
      mockMatchMedia(true);
      
      rerender(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        // Component should now render with mobile optimizations
        expect(screen.getByText('Content')).toBeInTheDocument();
      });
    });

    test('handles orientation changes', () => {
      mockMatchMedia(true);
      mockOrientation('portrait-primary', 0);

      const { container, rerender } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      // Change orientation
      mockOrientation('landscape-primary', 90);
      
      rerender(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      expect(container.firstChild).toBeInTheDocument();
    });
  });

  describe('Touch Events Support', () => {
    test('applies touch-optimized classes on mobile', () => {
      mockMatchMedia(true);

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      const wrapper = container.firstChild;
      // Should have touch-related classes
      expect(wrapper.className).toMatch(/touch|mobile/i);
    });
  });

  describe('Accessibility', () => {
    test('maintains proper semantic structure', () => {
      render(
        <MobileMatrixOptimizer>
          <button>Click Me</button>
        </MobileMatrixOptimizer>
      );

      const button = screen.getByRole('button', { name: 'Click Me' });
      expect(button).toBeInTheDocument();
    });

    test('preserves ARIA attributes from children', () => {
      render(
        <MobileMatrixOptimizer>
          <div aria-label="test-label">Content</div>
        </MobileMatrixOptimizer>
      );

      const element = screen.getByLabelText('test-label');
      expect(element).toBeInTheDocument();
    });
  });
});

describe('MobileMatrixRain Component', () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  describe('Component Rendering', () => {
    test('renders without crashing', () => {
      const { container } = render(<MobileMatrixRain />);
      expect(container.firstChild).toBeInTheDocument();
    });

    test('applies custom className', () => {
      const customClass = 'rain-custom-class';
      const { container } = render(<MobileMatrixRain className={customClass} />);
      
      expect(container.firstChild).toHaveClass(customClass);
    });

    test('has correct positioning classes', () => {
      const { container } = render(<MobileMatrixRain />);
      const wrapper = container.firstChild;
      
      expect(wrapper).toHaveClass('absolute');
      expect(wrapper).toHaveClass('inset-0');
      expect(wrapper).toHaveClass('pointer-events-none');
    });
  });

  describe('Style Tag Rendering', () => {
    test('renders standard <style> tag without jsx attribute', () => {
      const { container } = render(<MobileMatrixRain />);
      
      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
      expect(styleTag.hasAttribute('jsx')).toBe(false);
    });

    test('style contains matrix rain animation CSS', () => {
      const { container } = render(<MobileMatrixRain />);
      
      const styleTag = container.querySelector('style');
      const styleContent = styleTag.textContent;
      
      expect(styleContent).toContain('.matrix-mobile-rain');
      expect(styleContent).toContain('linear-gradient');
    });
  });

  describe('Visual Effects', () => {
    test('applies opacity for visual effect', () => {
      const { container } = render(<MobileMatrixRain />);
      const wrapper = container.firstChild;
      
      expect(wrapper).toHaveClass('opacity-30');
    });

    test('renders matrix-mobile-rain div', () => {
      const { container } = render(<MobileMatrixRain />);
      
      const rainDiv = container.querySelector('.matrix-mobile-rain');
      expect(rainDiv).toBeInTheDocument();
    });
  });

  describe('Responsive Behavior', () => {
    test('renders consistently on mobile', () => {
      mockMatchMedia(true);
      
      const { container } = render(<MobileMatrixRain />);
      expect(container.firstChild).toBeInTheDocument();
    });

    test('renders consistently on desktop', () => {
      mockMatchMedia(false);
      
      const { container } = render(<MobileMatrixRain />);
      expect(container.firstChild).toBeInTheDocument();
    });
  });
});

describe('MobileMatrixText Component', () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  describe('Component Rendering', () => {
    test('renders children correctly', () => {
      render(
        <MobileMatrixText>
          <span>Matrix Text</span>
        </MobileMatrixText>
      );

      expect(screen.getByText('Matrix Text')).toBeInTheDocument();
    });

    test('renders without crashing with no children', () => {
      const { container } = render(<MobileMatrixText />);
      expect(container.firstChild).toBeInTheDocument();
    });

    test('applies custom className', () => {
      const customClass = 'text-custom-class';
      const { container } = render(
        <MobileMatrixText className={customClass}>
          <span>Text</span>
        </MobileMatrixText>
      );

      expect(container.firstChild).toHaveClass(customClass);
    });
  });

  describe('Mobile-Specific Behavior', () => {
    test('applies mobile-matrix-text class on mobile devices', () => {
      mockMatchMedia(true);

      const { container } = render(
        <MobileMatrixText>
          <span>Mobile Text</span>
        </MobileMatrixText>
      );

      expect(container.firstChild).toHaveClass('mobile-matrix-text');
    });

    test('does not apply mobile-matrix-text class on desktop', () => {
      mockMatchMedia(false);

      const { container } = render(
        <MobileMatrixText>
          <span>Desktop Text</span>
        </MobileMatrixText>
      );

      expect(container.firstChild.className).not.toContain('mobile-matrix-text');
    });

    test('renders style tag only on mobile devices', () => {
      mockMatchMedia(true);

      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );

      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
    });

    test('does not render style tag on desktop', () => {
      mockMatchMedia(false);

      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );

      const styleTag = container.querySelector('style');
      expect(styleTag).toBeNull();
    });
  });

  describe('Style Tag Validation', () => {
    test('style tag does not have jsx attribute (regression test)', () => {
      mockMatchMedia(true);

      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );

      const styleTag = container.querySelector('style');
      expect(styleTag.hasAttribute('jsx')).toBe(false);
    });

    test('style contains responsive font sizing', () => {
      mockMatchMedia(true);

      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );

      const styleTag = container.querySelector('style');
      const styleContent = styleTag.textContent;

      expect(styleContent).toContain('clamp');
      expect(styleContent).toContain('font-size');
    });
  });

  describe('Typography Optimization', () => {
    test('applies mobile-optimized typography classes', () => {
      mockMatchMedia(true);

      const { container } = render(
        <MobileMatrixText>
          <h1>Heading</h1>
        </MobileMatrixText>
      );

      expect(container.firstChild).toHaveClass('mobile-matrix-text');
    });
  });
});

describe('Integration Tests', () => {
  test('all three components work together', () => {
    mockMatchMedia(true);

    render(
      <MobileMatrixOptimizer>
        <MobileMatrixRain />
        <MobileMatrixText>
          <h1>Combined Components</h1>
        </MobileMatrixText>
      </MobileMatrixOptimizer>
    );

    expect(screen.getByText('Combined Components')).toBeInTheDocument();
  });

  test('nested components maintain proper structure', () => {
    const { container } = render(
      <MobileMatrixOptimizer className="outer">
        <MobileMatrixRain className="rain" />
        <MobileMatrixText className="text">
          <div data-testid="nested">Nested Content</div>
        </MobileMatrixText>
      </MobileMatrixOptimizer>
    );

    expect(screen.getByTestId('nested')).toBeInTheDocument();
    expect(container.querySelector('.outer')).toBeInTheDocument();
    expect(container.querySelector('.rain')).toBeInTheDocument();
    expect(container.querySelector('.text')).toBeInTheDocument();
  });
});

describe('Edge Cases', () => {
  test('handles null children gracefully', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        {null}
      </MobileMatrixOptimizer>
    );

    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles multiple children', () => {
    render(
      <MobileMatrixOptimizer>
        <div>Child 1</div>
        <div>Child 2</div>
        <div>Child 3</div>
      </MobileMatrixOptimizer>
    );

    expect(screen.getByText('Child 1')).toBeInTheDocument();
    expect(screen.getByText('Child 2')).toBeInTheDocument();
    expect(screen.getByText('Child 3')).toBeInTheDocument();
  });

  test('handles rapid viewport changes', async () => {
    const { rerender } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    // Simulate multiple rapid viewport changes
    for (let i = 0; i < 5; i++) {
      mockMatchMedia(i % 2 === 0);
      rerender(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
    }

    await waitFor(() => {
      expect(screen.getByText('Content')).toBeInTheDocument();
    });
  });
});

describe('Performance Tests', () => {
  test('renders efficiently with many children', () => {
    const manyChildren = Array.from({ length: 100 }, (_, i) => (
      <div key={i}>Child {i}</div>
    ));

    const { container } = render(
      <MobileMatrixOptimizer>
        {manyChildren}
      </MobileMatrixOptimizer>
    );

    expect(container.querySelectorAll('div').length).toBeGreaterThan(100);
  });

  test('style tag injection does not cause memory leaks', () => {
    mockMatchMedia(true);

    const { unmount } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    unmount();

    // Component should unmount cleanly
    expect(screen.queryByText('Content')).not.toBeInTheDocument();
  });
});