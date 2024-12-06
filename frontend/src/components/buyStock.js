import React, { useState } from 'react';
import { Button, message } from 'antd';

const BuyStock = ({ symbol, shares, amount, tradeType }) => {
    const handleBuy = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/trade', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    symbol,
                    action: 'buy',
                    [tradeType]: tradeType === 'shares' ? parseFloat(shares) : parseFloat(amount)
                })
            });

            const data = await response.json();
            if (response.ok) {
                message.success(`Successfully bought ${symbol}`);
            } else {
                message.error(data.error);
            }
        } catch (error) {
            message.error('Failed to execute buy order');
        }
    };

    return (
        <Button 
            type="primary"
            onClick={handleBuy}
            style={{ width: '100%',
                color: 'white',
                backgroundColor: 'blue'
             }}
            disabled={!symbol || (tradeType === 'shares' ? !shares : !amount)}
        >
            Buy {symbol}
        </Button>
    );
};

export default BuyStock;
