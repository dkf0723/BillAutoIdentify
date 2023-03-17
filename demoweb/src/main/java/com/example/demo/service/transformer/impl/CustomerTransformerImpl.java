package com.example.demo.service.transformer.impl;

import com.example.demo.bean.CustomerBean;
import com.example.demo.entity.Customer;
import com.example.demo.entity.User;
import com.example.demo.service.transformer.CustomerTransformer;
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
