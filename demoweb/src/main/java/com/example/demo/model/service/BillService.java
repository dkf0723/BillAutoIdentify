package com.example.demo.model.service;

import com.example.demo.model.entity.Bill;
import org.springframework.stereotype.Service;

import java.util.List;

public interface BillService {
    List<Bill> findMistakeBill(int skip);
    List<Bill> findMistakeBill();
}
