with skolform as (
    select
        _dlt_parent_id  as dlt_parent_id
        ,string_agg(value , ', ') as skola_typ_kort
    from
        dlt_elin_testdata.students__handelses__elev__skola__skolformer
    group by
        _dlt_parent_id
),

student_step1 as (
    select
        substr( elev__person__personnummer,1,4) || '-' || substr( elev__person__personnummer,5,2) ||  '-' || substr( elev__person__personnummer,7,2) as födelsedag
        ,b.*
    from
                dlt_elin_testdata.students              as a
    left join   dlt_elin_testdata.students__handelses   as b on a._dlt_id = b._dlt_parent_id
),

student_final as (
    select
        '9999' || row_number() over( order by handelsedatum) as elev_id
        ,b.elev__skola__cs_nkod as org_id
        ,cast(b.handelsedatum as date)  as start_datum_skola
        ,'3900-01-01'                   as slut_datum_skola

        --Student
        ,födelsedag
        ,left(födelsedag,4) as födelseår
        ,case   when cast(substr(elev__person__personnummer,11,1) as int) %2 = 0    then 'Flicka'
                when cast(substr(elev__person__personnummer,11,1) as int) %2 = 1    then 'Pojke' end    as kön
        ,cast(floor((current_date - try_cast(födelsedag as date)) / 365.25 ) as int)                    as ålder
        ,case   when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 0 and 6 then '0-6'
                when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 7 and 10 then '7-10'
                when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 11 and 16 then '11-16'
                when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 17 and 20 then '17-20'
                when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 21 and 90 then '21+' end as ålders_grupp
        --Skola
        ,'Gymnasieskola'   as elev_gruppering
        ,case when skola_typ_kort = 'GY, GYAN' then 'Gymnasieskola anpassad' else 'Gymnasieskola' end as skola_typ
        ,s.skola_typ_kort
        ,b.elev__skola__namn    as skola_namn
        ,'G '|| b.elev__arskurs as årskurs
        ,null                   as klass
        ,0                      as is_elev_fritids
        -- Adress
        ,b.elev__person__folkbokforingsadress__postnummer   as post_kod
        ,b.elev__person__folkbokforingsadress__ort          as post_ort
        ,0 as is_pnr_error

        --Flaggor
        ,1 as is_aktiv_elev
        ,1 as is_öckerö_kommun
        ,0 as is_kommunal_verksamhet
        ,row_number() over (partition by elev__person__personnummer,handelsenamn, elev__arskurs order by handelsedatum desc) as  unique_row
    from
                student_step1   as b
    left join   skolform        as s on b._dlt_id = s.dlt_parent_id

    where
        handelsenamn ='Antagen'
)

select
    elev_id
    ,org_id
    ,start_datum_skola
    ,slut_datum_skola
    ,födelsedag
    ,födelseår
    ,kön
    ,ålder
    ,ålders_grupp
    ,elev_gruppering
    ,skola_typ
    ,skola_typ_kort
    ,skola_namn
    ,årskurs
    ,klass
    ,is_elev_fritids
    ,post_ort
    ,post_kod
    ,is_pnr_error
    ,is_aktiv_elev
    ,is_öckerö_kommun
    ,is_kommunal_verksamhet
from
    student_final
where
    unique_row = 1