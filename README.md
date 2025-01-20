## The Orac Reasoning Agent: LLM-based decision-making where there is little training data

This reasoning engine is designed to help solve problems where there might be insufficient data to train an LLC, so instead, a series of rules or heuristics are provided to the LLM to act as subject matter guidance.

Despite their power, Large Language Models struggle with specialized expert tasks where there is little or no trainable data. But what if we could teach them like we teach management consultants - using expert-created rules of thumb? This approach harnesses the LLM's general reasoning abilities but provides domain-specific guidance to provide high-quality results. 

This demo provides a series of "must do" and "must not do" conditions to the model specific to the particular task (domain) it has been given. In addition to any conditions in the user prompt, these rules provide additional guidance for how to handle the task.


<img width="613" alt="Xnapper-2025-01-15-14 19 03" src="https://github.com/user-attachments/assets/58f5c31a-1d36-49d7-b14f-f7631ad66a93" />


*Example of the model rejecting a scenario that doe not comply with the guidance*


Positive early tests applying this approach to corporate negotiations and geopolitical challenges show that this practical approach could unlock AI's potential in these high-value domains.

A demo of the first version is here

https://youtu.be/lZkC6iePuVQ

Update - 21/01/2025 

An updated version of the [demo is here](https://www.loom.com/share/2c47161005ee4a518b09a0b7856b4bf2?sid=38b06535-9ec7-4fda-b567-b11babde37e0) This shows the updated structure for the model output.

---
### Customization

The ```rules.py``` file contains the structure for you to add your own domain-specific rules. Fork the repo and then edit and amend these rules for your own domains. For best performance, try to write rules that are clearly provable/falsifiable and ensure that none of the rules contradict each other.  Rules are listed separately from the main heuristic to help keep this manageable and legible but are combined in the prompt to the model.

It can be useful to request the model to consider the 'must do' rules first, as this should provide the greatest number of options before eliminating those in the 'must not do' category.

---

### This is an open-source project

This software would not have been possible without the generosity of many in the security risk management and AI communities so, to maintain that spirit of openness, the code is being released under the GNU Affero General Public License. This is in the hope that many people will be able to benefit from this approach to decision-making and encourage others in the Security Risk Management space to take an equally collaborative approach.

Big thanks to [Replit](replit.com) for making such easy-to-use tools and to Karan (x: @karan4d) from [Nous Research](https://nousresearch.com) for introducing me to the idea of worldsim. 🙏

The repo is made available for testing and experimentation, and Decis Intelligence is not responsible for any loss, damage, injury, or outage resulting from the use of the tool's outputs.

(C) Decis Intelligence 2025
