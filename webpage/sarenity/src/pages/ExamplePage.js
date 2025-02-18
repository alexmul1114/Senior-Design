import React, { useState } from 'react';
import Grid from '../components/Grid';

const ExamplePage = () => {
  const [items, setItems] = useState([
    { id: 'item-1', x: 100, y: 100, render: () => <div style={{ background: '#eee', padding: '10px' }}>Item 1</div> },
    { id: 'item-2', x: 300, y: 200, render: () => <div style={{ background: '#ddd', padding: '10px' }}>Item 2</div> }
  ]);

  const handleItemPositionChange = (itemId, newX, newY) => {
    setItems(currentItems =>
      currentItems.map(item =>
        item.id === itemId ? { ...item, x: newX, y: newY } : item
      )
    );
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Example Page</h1>
      <p>This page includes a grid with a preset browser size. Items can be dragged around, and their positions are tracked.</p>
      <Grid
        sizePreset="1920x1080"
        items={items}
        onItemPositionChange={handleItemPositionChange}
      />

      <h2>Current Item Positions</h2>
      <pre>{JSON.stringify(items, null, 2)}</pre>
    </div>
  );
};

export default ExamplePage;
