import FormErrorItem from './FormErrorItem'
import './FormErrors.css'

export default function FormErrors(props) {
    let el_errors = null
    let el_errors_items = null


    if(props.errors.length > 0){
         el_errors_items = 
        props.errors.map(err_code => {
             <FormErrorItem err_code={err_code}/>
        })
        el_errors = (<div className='error' >
            {el_erros_items}
        </div>)
    }
    return (
        <div className='errorsWrap'>
{el_errors}
        </div>
    )
}