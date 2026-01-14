-- Set tidsram, 2 år till att starta med!
with params as (
    select
        cast(year(current_date)-1 || '-01-01' as date) as start_date
        ,cast(year(current_date) || '-12-31' as date) as end_date

),

-- Generate all dates between start and end
date_series as (
    select
        day as date_day
    from
        params, range(date_diff('day', start_date, end_date) + 1) as t(i)
    cross join LATERAL (
        select start_date + i * INTERVAL 1 DAY as day
    )
),

-- Add attributes
date_attributes as (
    select
        cast(date_day as date)  as date_key
        ,(year(date_day) || '-' || lpad(cast(month(date_day) as varchar), 2, '0')) AS year_month
        ,(year(date_day) || '-Q' || quarter(date_day))  as year_quarter
        ,year(date_day)         as year
        ,month(date_day)        as month
        ,day(date_day)          as day
    from
        date_series
)

    select
        *
        ,row_number() over( order by date_key desc)  as period_order
    from
        date_attributes
    where
        (day = '15' and month in(3,6,9,12)) -- Rapporten görs
    or date_key = current_date -- Få med dagens datum för att kunna få current!


--- Tanken här var att ta fram de datum som rapporten görs, skapa en periodkalender som man sedan joinar in studenter med hjälp av från och till datum
---- Dock fungerar de inte idag då vi inte har historik på var elever går!