

select * from   {{ref('raw_schoolsoft_students')}}  
union all
select * from   {{ref('raw_elin_students')}}  
