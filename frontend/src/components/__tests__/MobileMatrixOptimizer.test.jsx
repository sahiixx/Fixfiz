/**
 * Comprehensive unit tests for MobileMatrixOptimizer component
 * Testing the JSX style tag fix (migration from styled-jsx to standard React styles)
 * 
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  MobileMatrixRain, 
  MobileMatrixText 
} from '../MobileMatrixOptimizer';

// Mock window.matchMedia for mobile detection
const createMatchMediaMock = (matches) => () => ({
  matches,
  media: '',
  onchange: null,
  addListener: jest.fn(),
  removeListener: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  dispatchEvent: jest.fn(),
});

describe('MobileMatrixOptimizer', () => {
  beforeEach(() => {
    window.matchMedia = createMatchMediaMock(false);
  });

  describe('Component Rendering', () => {
    it('should render children correctly', () => {
      render(
        <MobileMatrixOptimizer>
          <div data-testid="child-content">Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByTestId('child-content')).toBeInTheDocument();
      expect(screen.getByTestId('child-content')).toHaveTextContent('Test Content');
    });

    it('should apply custom className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="custom-class">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('custom-class');
    });

    it('should render multiple children correctly', () => {
      render(
        <MobileMatrixOptimizer>
          <div data-testid="child1">Child 1</div>
          <div data-testid="child2">Child 2</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByTestId('child1')).toBeInTheDocument();
      expect(screen.getByTestId('child2')).toBeInTheDocument();
    });
  });

  describe('Style Tag Fix - JSX Attribute Warning Prevention', () => {
    it('should not render <style jsx> tags that cause React warnings', () => {
      window.matchMedia = createMatchMediaMock(true);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTags = container.querySelectorAll('style');
      styleTags.forEach(styleTag => {
        expect(styleTag).not.toHaveAttribute('jsx');
      });
    });

    it('should render standard <style> tags without jsx attribute', () => {
      window.matchMedia = createMatchMediaMock(true);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTags = container.querySelectorAll('style');
      styleTags.forEach(styleTag => {
        expect(styleTag.tagName).toBe('STYLE');
        expect(styleTag.hasAttribute('jsx')).toBe(false);
      });
    });

    it('should not create console warnings about jsx attribute', () => {
      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const jsxWarnings = consoleWarnSpy.mock.calls.filter(call => 
        call.some(arg => typeof arg === 'string' && arg.includes('jsx'))
      );
      expect(jsxWarnings.length).toBe(0);
      
      consoleWarnSpy.mockRestore();
    });
  });

  describe('Mobile Detection', () => {
    it('should apply mobile-optimized class on mobile viewport', () => {
      window.matchMedia = createMatchMediaMock(true);
      window.innerWidth = 375;
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    it('should not apply mobile classes on desktop', () => {
      window.matchMedia = createMatchMediaMock(false);
      window.innerWidth = 1920;
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).not.toHaveClass('mobile-optimized');
    });
  });

  describe('Edge Cases', () => {
    it('should handle null children gracefully', () => {
      expect(() => {
        render(<MobileMatrixOptimizer>{null}</MobileMatrixOptimizer>);
      }).not.toThrow();
    });

    it('should handle empty className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toBeDefined();
    });
  });
});

describe('MobileMatrixRain', () => {
  describe('Component Rendering', () => {
    it('should render without crashing', () => {
      expect(() => {
        render(<MobileMatrixRain />);
      }).not.toThrow();
    });

    it('should apply custom className', () => {
      const { container } = render(<MobileMatrixRain className="custom-rain" />);
      expect(container.firstChild).toHaveClass('custom-rain');
    });
  });

  describe('Style Tag Fix', () => {
    it('should not have jsx attribute on style tag', () => {
      const { container } = render(<MobileMatrixRain />);
      const styleTags = container.querySelectorAll('style');
      
      styleTags.forEach(styleTag => {
        expect(styleTag).not.toHaveAttribute('jsx');
      });
    });
  });
});

describe('MobileMatrixText', () => {
  describe('Component Rendering', () => {
    it('should render children correctly', () => {
      render(
        <MobileMatrixText>
          <span data-testid="text-content">Matrix Text</span>
        </MobileMatrixText>
      );
      
      expect(screen.getByTestId('text-content')).toBeInTheDocument();
    });

    it('should apply custom className', () => {
      const { container } = render(
        <MobileMatrixText className="custom-text">
          <span>Text</span>
        </MobileMatrixText>
      );
      
      expect(container.firstChild).toHaveClass('custom-text');
    });
  });

  describe('Style Tag Fix', () => {
    it('should not have jsx attribute on mobile style tag', () => {
      window.matchMedia = createMatchMediaMock(true);
      
      const { container } = render(
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      );
      
      const styleTags = container.querySelectorAll('style');
      styleTags.forEach(styleTag => {
        expect(styleTag).not.toHaveAttribute('jsx');
      });
    });
  });
});