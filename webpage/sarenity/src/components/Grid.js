import React, { useCallback } from 'react';

/**
 * Grid Component
 * 
 * Props:
 * - sizePreset: one of "1366x768", "1920x1080", "1536x864"
 * - items: an array of objects { id: string, x: number, y: number, render: () => JSX.Element }
 *          Each item defines its unique id, position, and a render function that returns the component.
 * - onItemPositionChange: a callback(itemId, newX, newY) to notify parent of position changes.
 * 
 * Behavior:
 * - Renders a fixed-size container based on sizePreset.
 * - Absolutely positions each item at (x, y).
 * - Allows dragging items around to update their coordinates.
 * 
 * Note: This example uses a simple mouse event-based dragging approach.
 * For more robust drag-and-drop, consider using a library like react-draggable.
 */

const SIZE_PRESETS = {
  "1366x768": { width: 1366, height: 768 },
  "1920x1080": { width: 1920, height: 1080 },
  "1536x864": { width: 1536, height: 864 }
};

const Grid = ({ sizePreset = "1366x768", items = [], onItemPositionChange }) => {
  const dimensions = SIZE_PRESETS[sizePreset] || SIZE_PRESETS["1366x768"];
  const { width, height } = dimensions;

  // Handle mouse events for dragging
  const handleMouseDown = useCallback((e, itemId) => {
    const startX = e.clientX;
    const startY = e.clientY;

    const target = e.currentTarget;
    const initialX = parseInt(target.getAttribute('data-x'), 10);
    const initialY = parseInt(target.getAttribute('data-y'), 10);

    const onMouseMove = (moveEvent) => {
      const deltaX = moveEvent.clientX - startX;
      const deltaY = moveEvent.clientY - startY;
      const newX = initialX + deltaX;
      const newY = initialY + deltaY;

      // Update element position visually
      target.style.transform = `translate(${newX}px, ${newY}px)`;
    };

    const onMouseUp = (upEvent) => {
      const endX = upEvent.clientX;
      const endY = upEvent.clientY;
      const deltaX = endX - startX;
      const deltaY = endY - startY;
      const finalX = initialX + deltaX;
      const finalY = initialY + deltaY;

      // Notify parent of final position
      if (onItemPositionChange) {
        onItemPositionChange(itemId, finalX, finalY);
      }

      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
  }, [onItemPositionChange]);

  return (
    <div 
      style={{
        position: 'relative',
        width: `${width}px`,
        height: `${height}px`,
        border: '1px solid #ccc',
        overflow: 'hidden',
        background: '#fafafa',
        userSelect: 'none' // disable text selection during drag
      }}
    >
      {items.map(item => (
        <div
          key={item.id}
          data-x={item.x}
          data-y={item.y}
          onMouseDown={(e) => handleMouseDown(e, item.id)}
          style={{
            position: 'absolute',
            cursor: 'grab',
            transform: `translate(${item.x}px, ${item.y}px)`
          }}
        >
          {item.render()}
        </div>
      ))}
    </div>
  );
};

export default Grid;