package com.example.demo.service;

import com.example.demo.entity.Bill;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface BillService {
    List<Bill> findMistakeBill();
}
