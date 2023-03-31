package com.example.demo.model.service.transformer;

import com.example.demo.model.bean.BillBean;
import com.example.demo.model.entity.Bill;
import org.springframework.stereotype.Component;
public interface BillTransformer extends BeanEntityTransformer<BillBean, Bill> {
}
