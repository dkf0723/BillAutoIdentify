package com.example.demo.model.service.impl;

import com.example.demo.model.bean.BillBean;
import com.example.demo.model.entity.Bill;
import com.example.demo.model.entity.BillDetail;
import com.example.demo.model.repository.BillDetailRepository;
import com.example.demo.model.repository.BillRepository;
import com.example.demo.model.service.BillService;
import com.example.demo.model.service.transformer.BillTransformer;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.beans.Beans;
import java.util.List;
@Service
public class BillServiceImpl implements BillService {
    @Autowired
    private BillDetailRepository billDetailRepository;
    @Autowired
    private BillRepository billRepository;
    @Autowired
    private BillTransformer transformer;
    private final int size = 1;
    @Override
    public BillBean findMistakeBill(int page) {
        Pageable pageable = PageRequest.of(page,size);
        List<Bill> bills =billRepository.findByCheckOrderByBillNumber("F",pageable);
        BillBean billBean = transformer.transferToBean(bills.get(0)) ;
        billBean.setBillDetailList(billDetailRepository.findByNumberOrderByColumn(billBean.getBillNumber()));
        billBean.setPage(page);
        return billBean;
    }

    @Override
    public BillBean findMistakeBill() {
        Pageable pageable = PageRequest.of(0,size);
        List<Bill> bills = billRepository.findByCheckOrderByBillNumber("F",pageable);
        BillBean billBean = transformer.transferToBean(bills.get(0)) ;
        billBean.setBillDetailList(billDetailRepository.findByNumberOrderByColumn(billBean.getBillNumber()));
        billBean.setPage(1);
        return billBean;
    }

}
