package com.example.demo.model.service;

import com.example.demo.model.bean.BillBean;
import com.example.demo.model.entity.Bill;
import org.springframework.stereotype.Service;

import java.util.List;

public interface BillService {
   BillBean findMistakeBill(int skip);
   BillBean findMistakeBill();
}
