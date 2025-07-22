calculations = {
    'balanceSheet': {
        'selected': [
            'cashAndEquivalents',
            'accountsReceivableNet', 
            'receivablesNetCurrent',
            'inventoryNet',
            'totalAssets',
            'goodwill',
            'intangibleAssetsIncludingGoodwill',
            'accumulatedDepreciationPpe',
            'currentLiabilities',
            'accountsPayable',
            'totalLiabilities',
            'longTermDebt',
            'stockholdersEquity',
            'currentAssets'
        ],
        'calculations': {
            'tangibleBookValue': 'stockholdersEquity - goodwill - intangibleAssetsIncludingGoodwill',
            'currentRatio': 'currentAssets / currentLiabilities',
            'debtToEquityRatio': 'totalLiabilities / stockholdersEquity',
            'bookValuePerShare': 'stockholdersEquity / commonSharesOutstanding',
            'tangibleBookValuePerShare': '(stockholdersEquity - goodwill - intangibleAssetsIncludingGoodwill) / commonSharesOutstanding'
        }
    },

    'incomeStatement': {
        'selected': [
            'totalRevenues',
            'costOfRevenue',
            'grossProfit',
            'interestExpense',
            'operatingIncome',
            'sgAExpense',
            'incomeContinuingOperations',
            'nonoperatingIncome',
            'netIncome',
            'netIncomeAvailableToCommonBasic',
            'pretaxIncomeContinuingOps',
            'incomeTaxContinuingOperations'
        ],
        'calculations': {
            'EBITDA': 'operatingIncome + depreciationAmortizationExpense',
            'netIncomeGrowth': '(netIncome - netIncome [year,-1]) / netIncome [year,-1]',
            'revenueGrowth': '(totalRevenues - totalRevenues [year,-1]) / totalRevenues [year,-1]',
            'operatingIncomeGrowth': '(operatingIncome - operatingIncome [year,-1]) / operatingIncome [year,-1]',
            'netIncomeContOpsGrowth': '(incomeContinuingOperations - incomeContinuingOperations [year,-1]) / incomeContinuingOperations [year,-1]',
            'returnOnAssets': 'netIncome / totalAssets',
            'returnOnEquity': 'netIncome / stockholdersEquity',
            'assetTurnover': 'totalRevenues / totalAssets'
        }
    },

    'CashFlowStatement': {
        'selected': [
            'accountsReceivableChange',
            'inventoryChange',
            'operatingCashFlow',
            'capex',
            'investingCashFlow',
            'commonStockCashDividends',
            'financingCashFlow',
            'fxEffectOnCash',
            'cashChangePeriod',
        ],
        'calculations': {
            'freeCashFlow': 'operatingCashFlow - capex',
            'operatingCashFlowMargin': 'operatingCashFlow / totalRevenues',
            'freeCashFlowMargin': 'freeCashFlow / totalRevenues',
            'capexAsPercentOfRevenue': 'capex / totalRevenues'
        }
    },

    'earningsReport': {
        'selected': [
            'weightedAvgSharesBasic',
            'weightedAvgSharesDiluted',
            'epsDiluted',
            'commonSharesOutstanding'
        ],
        'calculations': {
            'dividendPerShare': 'commonStockCashDividends / weightedAvgSharesBasic',
            'basicContinuousOperations': 'incomeContinuingOperations / weightedAvgSharesBasic',
            'continuingAndDiscontinuedBasicEPS': 'netIncome / weightedAvgSharesBasic',
            'continuingAndDiscontinuedDilutedEPS': 'netIncome / weightedAvgSharesDiluted',
            'dilutedContinuousOperations': 'incomeContinuingOperations / weightedAvgSharesDiluted'
        }
    },

    'OperationRatios': {
        'selected': [],
        'calculations': {
            'grossMargin': 'grossProfit / totalRevenues',
            'operationMargin': 'operatingIncome / totalRevenues',
            'netMargin': 'netIncome / totalRevenues',
            'EBITMargin': 'operatingIncome / totalRevenues',
            'interestCoverage': 'operatingIncome / interestExpense',
            'EBITDAMargin': '(operatingIncome + depreciationAmortizationExpense) / totalRevenues',
            'effectiveTaxRate': 'incomeTaxContinuingOperations / pretaxIncomeContinuingOps',
            'pretaxMargin': 'pretaxIncomeContinuingOps / totalRevenues',
            'normalizedNetProfitMargin': 'netIncome / totalRevenues'
        }
    }
}