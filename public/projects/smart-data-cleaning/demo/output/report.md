# Smart Data Cleaning + Reporting

## Execution summary
- Rows (raw): 123,600
- Rows (clean): 118,772
- Dropped: 4,828
- Duplicates removed (estimate): 3,600
- Missing cells (raw): 3,708
- Missing cells (clean): 120,580

## KPI snapshot
- **orders**: 115620
- **customers**: 70171
- **products**: 17415
- **total_value**: 372620.57999999996
- **aov**: 3.222803840166062
- **repeat_rate**: 0.3652363511992133

## Top departments (by items)
- produce: 34453
- dairy eggs: 20022
- snacks: 10525
- beverages: 9888
- frozen: 8032

## Data quality notes (top missing columns)
- order_hour: 118772
- product_name: 617
- aisle: 596
- department: 595

## Rules applied / notes
- Renamed column 'Order ID' -> 'order_id'
- Renamed column 'CustomerID' -> 'user_id'
- Renamed column 'OrderDate' -> 'order_date'
- Renamed column 'Unit Price' -> 'unit_price'
- Renamed column 'Order Value' -> 'order_value'
- Removed duplicates on (order_id, product_id): 3600
- Dropped rows missing critical fields ['order_id', 'user_id', 'product_id', 'order_date']: 614
- Dropped rows with invalid unit_price: 614
- Rows: 123600 -> 118772 (delta -4828)
