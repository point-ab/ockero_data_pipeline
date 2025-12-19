
{{config(enabled=false)}}


with student_step1 as (
    -- Förbered födelsedatum
    select
        cast(case   when left(socialnumber,1)  > left(cast(current_date as varchar),1)
                then '19' || substr(socialnumber, 1, 2)
                else '20' || substr(socialnumber, 1, 2) end as int) as födelseår
        ,case   when left(socialnumber,1)  > left(cast(current_date as varchar),1)
                then '19' || substr(socialnumber, 1, 2)
                else '20' || substr(socialnumber, 1, 2) end
        || '-' || substr(socialnumber, 3, 2)
        || '-' || substr(socialnumber, 5, 2) as  födelsedag
        ,*
    from
        dlt_schoolsoft.students
),

student_step2 as (
    select
        *
        ,case   when substring(pocode,1,3) ='475' then 1
                when pocode in ('430 90' --Öckerö
                                ,'430 93' --Hälsö
                                ,'430 94' --Bohus‑Björkö
                                ,'430 95' --Källö‑Knippla
                                ,'430 92' --Fotö
                                ,'430 97' --Rörö
                                ,'430 96' --Hyppeln
                                )
                                then 1 else 0 end as is_öckerö_kommun 
    from
        student_step1
),

student_final as (
    select
        id          as elev_id
        ,orgid      as org_id

        ,case when startdate = ''  then null            else startdate  end as start_datum_skola
        ,case when enddate = ''    then '3999-01-01'    else enddate    end as slut_datum_skola

        --Student
        ,födelsedag
        ,födelseår
        ,case   when sex = 'f'  then 'Flicka'
                when sex = 'p'  then 'Pojke'  end   as kön
        ,cast(floor((current_date - try_cast(födelsedag as date)) / 365.25 ) as int)   as ålder
        ,case   when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 0 and 6 then '0-6'
                when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 7 and 10 then '7-10'
                when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 11 and 16 then '11-16'
                when floor((current_date - try_cast(födelsedag as date)) / 365.25 ) between 17 and 80 then '16+' end as ålders_grupp

        -- Skola
        ,case   when month(current_date) >= 8   and födelseår >= year(current_date) - 5 then 'Förskola'
                when month(current_date) < 8    and födelseår >= year(current_date) - 6 then 'Förskola'
                when födelseår >= year(current_date) - 15 and schooltype = 'GR11'       then 'Grundskola'
                when födelseår >= year(current_date) - 15 and schooltype = 'GRAN'       then 'Grundskola anpassad'
                when schooltype in('GY11','GY25')                                       then 'Gymnasieskola' end as elev_gruppering
           
        ,case   when schooltype = 'BO'   then 'Förskola'
                when schooltype = 'GR11' then 'Grundskola'
                when schooltype = 'GRAN' then 'Grundskola anpassad'
                when schooltype = 'GY11' then 'Gymnasieskola'
                when schooltype = 'GY25' then 'Gymnasieskola' end as  skola_typ
        ,schooltype     as skola_typ_kort       
        ,schoolname     as skola_namn
        ,case   when schooltype in('GY11','GY25')       then 'G '|| year
                when year = '' and schooltype in('BO')  then 'F'        else year end as årskurs
        ,class          as klass
        ,leisureschool  as is_elev_fritids
        
        -- Adress
        ,city
        ,pocode as post_kod
        ,case when try_cast(födelsedag as date) is null then 1 else 0 end as is_pnr_error

        --Flaggor
        ,active     as is_aktiv_elev
        ,is_öckerö_kommun -- fix
        ,case   when o.is_kommunal = 1 and schooltype in ('GR11','GRAN') and årskurs = '' then 0 else o.is_kommunal end as is_kommunal_verksamhet
    from
                student_step2                   as s
    left join   {{ref('schoolsoft_schools')}}   as o on s.orgid = o.org_id

    where
        ålder < 25
)

select * from student_final



--- Få åldersgrupperingar till perioden? Kanske är svårt?
-- Hårdkoda lika tidsperioder, alltså ta fram varje kvartalsslut istället?
-- Det gör att vi kan se senaste kvartal vad en person var och hade!