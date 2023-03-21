package com.example.demo.model.service.impl;

import com.example.demo.model.entity.Bill;
import com.example.demo.model.repository.BillRepository;
import com.example.demo.model.service.BillService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class BillServiceImpl implements BillService {
    @Autowired
    private BillRepository billRepository;
    private final int size = 1;
    @Override
    public List<Bill> findMistakeBill(int skip) {
        Pageable pageable = PageRequest.of(skip,size);
        return billRepository.findByCheckOrderByBillNumber("F",pageable);
    }

    @Override
    public List<Bill> findMistakeBill() {
        Pageable pageable = PageRequest.of(0,size);
        return billRepository.findByCheckOrderByBillNumber("F",pageable);
    }

}
