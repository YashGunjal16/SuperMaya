// src/components/VegaChart.jsx
import React from 'react';
import { VegaLite } from 'react-vega';

export default function VegaChart({ spec }) {
    // Add a dark theme configuration to the spec
    const themedSpec = {
        ...spec,
        config: {
            background: '#2d2d2d',
            title: { color: '#e0e0e0' },
            style: {
                'guide-label': {
                    fill: '#a0a0a0'
                },
                'guide-title': {
                    fill: '#e0e0e0'
                }
            },
            axis: {
                domainColor: '#a0a0a0',
                gridColor: 'rgba(255, 255, 255, 0.1)',
                tickColor: '#a0a0a0'
            },
            legend: {
                labelColor: '#e0e0e0',
                titleColor: '#e0e0e0'
            }
        }
    };

    return (
        <div className="chart-wrapper">
            <VegaLite spec={themedSpec} actions={false} />
        </div>
    );
}