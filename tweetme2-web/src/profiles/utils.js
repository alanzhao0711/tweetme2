import React from 'react'
import numeral from 'numeral'

export function DisPlayCount(props){
    return <span className={props.className}>{numeral(props.children).format("0a")}</span>
  }
  