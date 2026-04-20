import { useState } from "react"

export const useForm = (initialState) => {
  const [values, setValues] = useState(initialState)
  
  const onChange = (event) => {
    const { name, value } = event.target

    setValues(prev => ({
      ...prev,
      [name]: value
    }))
  }

  return [values, onChange]
}