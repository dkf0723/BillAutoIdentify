package com.example.demo.model.service.transformer.impl;

import com.example.demo.model.bean.CustomerBean;
import com.example.demo.model.entity.Customer;
import com.example.demo.model.service.transformer.CustomerTransformer;
import org.springframework.beans.BeanUtils;

public class CustomerTransformerImpl implements CustomerTransformer {
    @Override
    public Customer transferToEntity(CustomerBean customerBean) {
        Customer customer = new Customer();
        BeanUtils.copyProperties(customerBean, customer);
        return customer;
    }

    @Override
    public CustomerBean transferToBean(Customer customer) {
        CustomerBean customerBean = new CustomerBean();
        BeanUtils.copyProperties(customer, customerBean);
        return customerBean;
    }
}
