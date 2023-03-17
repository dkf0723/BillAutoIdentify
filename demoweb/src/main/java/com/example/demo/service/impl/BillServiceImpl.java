package com.example.demo.service.impl;

import com.example.demo.entity.Bill;
import com.example.demo.repository.BillRepository;
import com.example.demo.service.BillService;
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
