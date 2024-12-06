import React, { useState } from 'react';
import { Button, message } from 'antd';

const SellStock = ({ symbol, shares, amount, tradeType }) => {
    const handleSell = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/trade', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    symbol,
                    action: 'sell',
                    [tradeType]: tradeType === 'shares' ? parseFloat(shares) : parseFloat(amount)
                })
            });

            const data = await response.json();
            if (response.ok) {
                message.success(`Successfully sold ${symbol}`);
            } else {
                message.error(data.error);
            }
        } catch (error) {
            message.error('Failed to execute sell order');
        }
    };

    return (
        <Button 
            type="danger"
            onClick={handleSell}
            style={{ width: '100%',
                color: 'white',
                backgroundColor: 'red'
             }}
            disabled={!symbol || (tradeType === 'shares' ? !shares : !amount)}
        >
            Sell {symbol}
        </Button>
    );
};

export default SellStock;
