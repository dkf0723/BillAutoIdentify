package com.example.demo.model.service.impl;

import com.example.demo.model.entity.Bill;
import com.example.demo.model.repository.BillRepository;
import com.example.demo.model.service.BillService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class BillServiceImpl implements BillService {
    @Autowired
    private BillRepository billRepository;
    @Override
    public List<Bill> findMistakeBill() {

        return billRepository.findByCheck("F");
    }
}
